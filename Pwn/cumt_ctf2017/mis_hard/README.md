

## 好像出难了

思路，主要就是特殊的lsb放在图片里面，然后属性里面给了base64编码的提示，解出来之后是arm的汇编。。<br>
我是把它按4bytes一组按小端扣出来(arm指令等长)<br>
然后也给了地址，所以写个脚本写进文件(主要大端小端问题)

## 分析

arm汇编其实慢慢看也可以的，就两个循环，猜猜看大概就是矩阵乘法了<br>

把矩阵扣出来求个逆，然后就是对应的falg的ascii了<br>

下面是写文件的脚本，我是把偏移减去了0x00010000，实际上之后ida加载可以再指定加上0x00010000。<br>
不过最方便的还是就是直接写绝对地址就好(就是文件可能稍微大了点)

```Python
from pwn import *

fp_code = open("mcode.txt", "rb")
fp_data = open("mdata.txt", "rb")
fp_wri = open("res.bin", "w")

elf_base = 0x00010000

fp_wri.seek(0x00000554)
for line in fp_code.readlines():
    line = line.strip('\n')
    opc_list = line.split(' ')
    opcode = p32(int(opc_list[0], 16))
    fp_wri.write(opcode)
    if len(opc_list)==2:
        opcode = p32(int(opc_list[1], 16))
        fp_wri.write(opcode)

fp_wri.seek(0x0001102C)
for line in fp_data.readlines():
    line = line.strip('\n')
    print line
    opc_list = line.split(' ')
    opcode = p32(int(opc_list[0], 16))
    fp_wri.write(opcode)
    opcode = p32(int(opc_list[1], 16))
    fp_wri.write(opcode)

fp_code.close()
fp_data.close()
fp_wri.close()

```

## Tips

1. 求逆矩阵用matlab什么的就好
2. 有人说我白学，看到有白学的题就是我出的，然后就不做。。哎，畏难心理真不好，总得看看题吧。
> 熟练无罪，白学万岁23333
