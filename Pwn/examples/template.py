from pwn import *
import time, sys


# local process envirnoment
LOCAL = False
elf_name = "./pwn"

#retmote args
remote_host = "127.0.0.1"
remote_port = 50002
context.clear(arch="amd64")
elf = ELF(elf_name)

if LOCAL:
    smlbin_area_off = 0x3C3B78
    execv_binsh_off = 0xF0567
    malloc_hook_off = 0x3C3B10
    context.log_level = "debug"
    mine_env = os.environ
    mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so"
    io = process(elf_name, env=mine_env)
else:
    #context.log_level = "debug"
    smlbin_area_off = 0x3C3B78
    execv_binsh_off = 0xF0567
    malloc_hook_off = 0x3C3B10
    io = remote(remote_host, remote_port)

def dlySend(sdstr):
    io.send(sdstr)
    time.sleep(0.01)

def mmenu(mindex):
    io.recvuntil("\n")
    io.sendline(str(mindex))

def s_exp():
    print io.recvall()

if __name__ == "__main__":
    s_exp()
    #pause()
