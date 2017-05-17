from pwn import *
import time


run_argv = []
# local process envirnoment
LOCAL = True
elf_name = "./houseoforange"

#retmote args
remote_host = "127.0.0.1"
remote_port = 22333

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
    io = remote(remote_host, remote_port)


def s_leak():
    lk_data = 0
    return lk_data

def s_exp():
    lk_data = s_leak()

if __name__ == "__main__":
    raw_input("start")
    s_exp()
    raw_input("end")
