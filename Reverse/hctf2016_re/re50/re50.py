#coding:utf-8



'''

B1 00 00 00 A4 00 00 00  B5 00 00 00 87 00 00 00

AD 00 00 00 AD 00 00 00  93 00 00 00 B9 00 00 00

BF 00 00 00 BF 00 00 00  93 00 00 00 FD 00 00 00

FC 00 00 00 B8 00 00 00  FF 00 00 00 B7 00 00 00

F9 00 00 00 B8 00 00 00  ED 00 00 00 A4 00 00 00

'''

alph = [0xB1, 0xA4, 0xB5, 0x87, 0xAD, 0xAD, 0x93, 0xB9, 0xBF, 0xBF, 0x93, 0xFD, 0xFC, 0xB8, 0xFF, 0xB7, 0xF9, 0xB8, 0xED, 0xA4]

flag_test = ''
flg_fake = []

for i in alph:
    flg_fake.append(i^0xCC)

for i in range(5):
    tmp = flg_fake[2*i]
    flg_fake[2*i] = flg_fake[19-2*i]
    flg_fake[19-2*i] = tmp

flg_fake[9] = flg_fake[7] - 2
flg_fake[7] = flg_fake[5] - 2
flg_fake[5] = flg_fake[3] - 2
flg_fake[3] = flg_fake[1] - 2

for c in flg_fake:
    flag_test += chr(c)

print flag_test

