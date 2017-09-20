
## ptrace
用于监视进程的系统调用，sandbox中用这个限制了一些系统调用

```
11	sys_execve
5	sys_open
120	sys_clone
190	sys_vfork
295	sys_openat
8	sys_creat
```

## 32bit to 64bit
`syscall`中，32bit和64bit调用号是不一样的，可以转成64bit进行函数调用，汇编如下

```asm

// "\x6a\x33\xe8\x00\x00\x00\x00\x83\x04\x24\x05\xcb"
push 0x33
push ip
retf
```
