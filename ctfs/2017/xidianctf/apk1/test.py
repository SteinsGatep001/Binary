import hashlib, base64

org_str = "xianRE"

org_list = ""
for c in org_str:
    org_list += chr(ord(c)^0x01)
    print chr(ord(c)^0x01)

print org_list
m2 = hashlib.md5()
m2.update(org_list)
print m2.hexdigest()


res_str = "NWJiNGRjMzMwMmVjNDkzODI4MjdkMDk2MjRkZjZhYzg="
#res_str = "YmZhODE3OThlMzZmMzFhYzcyYTdkOWE0N2RjY2Y4YzU="
resad_s = ""
for c in res_str:
    resad_s += chr(ord(c)^2)
print resad_s


flag = "it4;eseQzdSxwEkhvwPTGe??"
res = ""
for c in flag:
    res += chr(ord(c)^2)
print res

bs64_nstr = "kv69gqgSxfQzuGijtuRVEg=="
hex_b44 = base64.b64decode(bs64_nstr)

for c in hex_b44:
    print hex(ord(c)), chr(ord(c)^1)
