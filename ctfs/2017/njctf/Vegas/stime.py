import os
import time
from pwn import *

mine_time = int(time.time())


mine_env = os.environ
mine_env['LD_PRELOAD'] = './desrand64.so'

mine_env['SEED'] = str(mine_time)
io0 = process('./stime')
print 'io0:'
print io0.recvall()
io0.clean()
sleep(1)

mine_env['SEED'] = str(mine_time)
io1 = process('./stime', env=mine_env)
print 'io1'
print io1.recvall()
io0.clean()

io0.close()
io1.close()


