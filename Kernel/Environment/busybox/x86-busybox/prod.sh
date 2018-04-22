#!/bin/sh

find . -print0 \
    | cpio --null -ov --format=newc \
    | gzip -9 > /tmp/initramfs-busybox-x86.cpio.gz

