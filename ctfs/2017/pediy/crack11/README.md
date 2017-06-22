
## load pe

0x4473A8跳转到解密好的程序
0x401690为真正的程序主流程

## check

```C
if(c-'a'>25)
{
    if(c-'A'<=25)
        tmp = c-36;
}
else
    tmp = c-'a'+1
tmp_res = 3 * tmp % 52
if ( tmp_res - 27 <= 25 )
    updt_c = tmp_res + 38;
else if ( tmp_res - 1 <= 25 )
    updt_c = tmp_res + 96;
res += (0x132 - i + updt_c) ^ (0x132 - i + 0x61)
```
最后判断res == 0x127514D
