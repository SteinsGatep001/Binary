
## Resources

1. [linux kernel exploitation](https://github.com/xairy/linux-kernel-exploitation)

## debug

### symbol
如果`module`没有去`symbol`，可以加载下`symbol`方便调试
```
add-symbol-file example.ko [address]
```

### find function address

in `busybox`
```
grep prepare_kernel_cred /proc/kallsyms
```

## basic

提权
```C
commit_creds(prepare_kernel_cred(0));
```

## To be continued

