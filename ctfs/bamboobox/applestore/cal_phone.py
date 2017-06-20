
res = 7174

tmp = 0;
for i1 in range(40):
    tmp1 = i1*199
    for i2 in range(24):
        tmp2 = i2*299
        for i3 in range(18):
            tmp3 = i3*399
            for i4 in range(16):
                tmp4 = i4*499
                tmp = tmp1+tmp2+tmp3+tmp4
                if tmp == res:
                    print i1, i2, i3, i4
