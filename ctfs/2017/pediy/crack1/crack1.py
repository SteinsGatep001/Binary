

for i in range(10):
    for j in range(10):
        res = (i-0.2)*j*16
        if res<385 and res>383:
            print i, j, res
#((c3-'0') - 0.2)*(c4-'0') = 24
