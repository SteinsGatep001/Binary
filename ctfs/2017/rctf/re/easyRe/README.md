
## Preface

调试调试 orz


## Dbg

再0x08048478断下

然后dump内存
```C
auto file, fname, i, address, size, x;
address = 0xF770B000;
size = 0x001D74;
fname = "dump_mem.bin";
file = fopen(fname, "wb");
for (i=0; i<size; i++, address++)
{
 x = DbgByte(address);
 fputc(x, file);
}
fclose(file);
```
dump_mem.bin 拖入ida<br>

然后解密<br>
```Python
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
```
