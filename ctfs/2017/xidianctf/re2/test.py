
# 0x04015D0
# a2 % 5 != 3 || a2 % 7 != 2 || a2 % 13 != 4;

# 303.12345
# 4
# tmp = buf[i%len1] + part2[i] - 0x30
# (tmp + (tmp&0x0F)) >> 4 high4
# low4

for c in range(0x30, 0x80):
    print chr(c)

cmp_list = [0x35,0x44,0x34,0x41,\
0x34,0x37,0x35,0x39,0x34,0x37,0x37,\
0x44,0x34,0x43,0x36,0x38,0x33,0x36,0x37,0x32,\
0x33,0x34,0x33,0x37,\
0x33,0x31,0x36,0x45,0x33,0x42,0x36,0x45,0x37,0x31,0x37,0x41,0x37,0x38,0x37,0x45,0x37,0x34,0x37,0x46]
print len(cmp_list)

mstrip_list = [',', '.', '|', '[', ']', '@', '\\', '/', ' ', '?', '~', '-', ';', '>', '<', '+', '*', ')']

def print_reflag(key_str):
    flag_str = ""
    for i in range(len(cmp_list)/2):
        res_list = []
        for c in range(0x30, 0x80):
            tmp = ord(key_str[i%len(key_str)]) + c - 0x30
            part1 = (tmp>>4) & 0x0F
            part2 = tmp&0x0F
            if part1>0x09:
                part1+=0x37
            else:
                part1+=0x30

            if part2>0x09:
                part2+=0x37
            else:
                part2+=0x30
            if cmp_list[i*2] == part1 and cmp_list[i*2+1] == part2:
                res_list.append(chr(c))
        #print res_list
        if len(res_list) == 0:
            return
        else:
            flag_str += res_list[0]
    '''
    not_vldflag = True
    for m in mstrip_list:
        if m in flag_str:
            not_vldflag = False
            break
    if not_vldflag:
    '''
    if 'XDCTF' in flag_str:
        print key_str+'.'+flag_str

def calflag(key_str):
    flag_str = ""
    for i in range(len(cmp_list)/2):
        part1 = cmp_list[2*i]
        part2 = cmp_list[2*i+1]
        if part1<=0x39:
            part1-=0x30
        else:
            part1-=0x37

        if part2>0x39:
            part2-=0x30
        else:
            part2-=0x37

        now_func = (part1<<4) | part2

        now_func &= 0xFF

        res = now_func+0x30-ord(key_str[i%len(key_str)])

        # print "[dbg]", i, hex(part1), hex(part2), hex(res), chr(res)

        flag_str += chr(res)

    print flag_str

for i in range(0, 0xFFFFFFF):
    if i%5==3 and i%7==2 and i%13==4:
        #print "part1:", i
        print_reflag(str(i))
