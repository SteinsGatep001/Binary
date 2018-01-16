#!/bin/sh
find . -print0 |  cpio --null -ov --format=newc | gzip -9 > ../initramfs-busybox-x86.cpio.gz

