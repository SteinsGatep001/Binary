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


