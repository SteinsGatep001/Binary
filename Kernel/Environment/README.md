# Eat Sleep Ring0


## Environment

手动下载需要版本的源码，然后进行编译。（遇到问题google基本能解决）


### qemu-system

要让qemu能跑起来，并调试内核，需要
```bash
qemu-system-i386 -nographic -kernel ./linux-2.6.32.1/arch/i386/boot/bzImage -append "console=ttyS0 rw ip=dhcp init=/sbin/init" -initrd ./busybox-1.19.4/initramfs-busybox-x86.cpio.gz -gdb tcp::1234 -S
```

具体操作：
1. `gdb vmlinux`(vmlinux是编译linux的时候产生的符合表)，然后`target remote localhost:1234`
2. 启动`run.sh`，也就是启动`qemu`虚拟机
3. 在gdb下断点，然后就可以调试了




