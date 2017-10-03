import base64

resStr = "KxU+NEhUEFVBaWB4HUAyVgZ3ZnlLamAHAUUHR20zJlk="

keyEn = "My_S3cr3t_P@$$W0rD\x00"

tmp = base64.b64decode(resStr)


out_R = ""
print len(tmp), len(keyEn)
for i in range(len(tmp)):
    c = ord(tmp[i])^ord(keyEn[i%18])
    out_R += chr(c)

print out_R
