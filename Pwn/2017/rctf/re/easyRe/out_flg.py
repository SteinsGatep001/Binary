

org_string = "69800876143568214356928753"

res = ""

res += chr(2*ord(org_string[1]))
res += chr(ord(org_string[4])+ord(org_string[5]))
res += chr(ord(org_string[8])+ord(org_string[9]))
res += chr(ord(org_string[12])+ord(org_string[12]))
res += chr(ord(org_string[18])+ord(org_string[17]))
res += chr(ord(org_string[10])+ord(org_string[21]))
res += chr(ord(org_string[9])+ord(org_string[25]))

print res
