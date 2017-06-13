#coding:utf-8
alph1 = "onhtxdsqvpzcrefjigklfzbapvdqsxzrcefimlku"
alph2 = "zscbmdvholblzftuhsxsbchanrcdqjvqfinotcbu"
alph3 = "pzywrvdcbqeuafsxgmlitnkopvdqsxtdnapcuwys"

username = "041751300132"
pwd1 = ""
pwd2 = ""
pwd3 = ""

ad1_1 = 0
ad1_2 = 0
ad1 = 10*(ad1_1 + 2 * ad1_2)
#10 * (bIsIda + 2 * bOD_52pojie)
ad2_1 = 1
ad2_2 = 1
ad2 = 10*(ad2_1 + 2 * ad2_2)
#5 * (v3 + 2 * v2) + 2
ad3_1 = 0
ad3_2 = 1
ad3 = 10*(ad3_1 + 2 * ad3_2)

password = ""

for s in username:
    index = int(s)
    pwd1 += alph2[ad1+index]
    pwd2 += alph3[ad2+index]
    pwd3 += alph1[ad3+index]

passwd = pwd1[0:4] + pwd2[4:8] + pwd3[8:12]

for s in passwd:
    if s == 'z':
        password += 'a'
    else:
        password += chr(ord(s) + 1)

print password


