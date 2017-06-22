

min_str = "aA"
res = 0
i=0
updt_c = 0
tmp = 0

for i in range(len(min_str)):
    c = ord(min_str[i])
    if c-ord('a')>25 or c-ord('a')<0:
        if c-ord('A')<=25 :
            tmp = c-36
    else:
        tmp = c-ord('a')+1
    tmp_res = (3*tmp) % 52
    if tmp_res - 27 <= 25 and tmp_res >= 27:
        updt_c = tmp_res + 38
    else:
        if tmp_res - 1 <= 25 :
            updt_c = tmp_res + 96
    tmp1 = (0x39D347 - i + updt_c)&0xFF
    tmp2 = (0x39D347 - i + 0x61)&0xFF
    print(hex(tmp),hex(updt_c),hex(tmp1),hex(tmp2))
    res += tmp1^tmp2

print(hex(res))
