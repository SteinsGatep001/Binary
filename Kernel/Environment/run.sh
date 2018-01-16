#!/bin/sh
#qemu-system-i386 -kernel ./linux-2.6.32.1/arch/i386/boot/bzImage -initrd ./busybox-1.19.4/initramfs-busybox-x86.cpio.gz -nographic -append "console=ttyS0"
#qemu-system-i386 -kernel ./linux-2.6.32.1/arch/i386/boot/bzImage -initrd ./busybox-1.19.4/initramfs-busybox-x86.cpio.gz -nographic -append "root=/dev/ram rdinit=/sbin/init"
qemu-system-i386 -nographic -kernel ./linux-2.6.32.1/arch/i386/boot/bzImage -append "console=ttyS0 rw ip=dhcp init=/sbin/init" -initrd ./busybox-1.19.4/initramfs-busybox-x86.cpio.gz -gdb tcp::1234 -S

