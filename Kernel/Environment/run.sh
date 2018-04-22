#!/bin/sh

qemu-system-x86_64 \
    -kernel obj/linux-x86-basic/arch/x86_64/boot/bzImage \
    -initrd /tmp/initramfs-busybox-x86.cpio.gz \
    -nographic -append "console=ttyS0 quiet" \
    -monitor /dev/null \
    -nographic \
    2>/dev/null

