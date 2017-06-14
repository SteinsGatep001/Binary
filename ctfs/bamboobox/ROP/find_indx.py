
fp = open("main.asm", "rb")

res = ""
for line in fp.readlines():
    if ';' in line:
        print line
        res += line.strip('\n')
fp.close()

# 1,13,11,9,3,3,12,4,13,2,13,2,8,8,0,13,13,13,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,13,13,13,6,9,12,4,13,4,4,7,0,3,3,3,3,3,3,3,3,1,12,7,7,8,8,0
res = "SECPROG{return_oriented_program"
print(len(res))
