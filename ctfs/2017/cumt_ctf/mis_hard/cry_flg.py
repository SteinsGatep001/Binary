from pwn import *


def read_martix(filename, rd_rows):
    fp = open(filename, "r")
    martix_res = [[] for i in range(rd_rows)]
    index = 0
    for line in fp.readlines():
        mt_list = line.strip('\n').split(' ')
        for i in range(rd_rows):
            martix_res[index].append(int(mt_list[i], 10))
        index += 1
    fp.close()
    return martix_res

def cal_martix_val(key_mtx, rows, val_list):
    res_list = []
    for i in range(rows):
        tmp_res = 0
        for j in range(rows):
            tmp_res += val_list[j] * key_mtx[i][j];
        res_list.append(tmp_res)
    return res_list

flag_txt = "mart1x_m1sc_233"
flag_len = len(flag_txt)

flag_ord_list = []
for i in range(flag_len):
    flag_ord_list.append(ord(flag_txt[i]))
print "flag ord list: ", flag_ord_list

martix_encrypt = read_martix("mtun0.txt", flag_len)
martix_decrypt = read_martix("dtun0.txt", flag_len)
'''
for i in range(flag_len):
    print martix_encrypt[i]
for i in range(flag_len):
    print martix_decrypt[i]
'''
flag_cryptlist = cal_martix_val(martix_encrypt, flag_len, flag_ord_list)
print "crypted ord list: ", flag_cryptlist
print cal_martix_val(martix_decrypt, flag_len, flag_cryptlist)

