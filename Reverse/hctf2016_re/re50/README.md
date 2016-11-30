#

## 调试
ida直接打开分析不出函数名，不过也比较简单，所以直接调试
```C++
v19 = xmmword_13F7480;
v20 = xmmword_13F74B0;
v21 = xmmword_13F74C0;
v22 = xmmword_13F74A0;
v23 = xmmword_13F7490;
sub_13E1F00(&v24, 0, 120);
printf("Input Your Flag:", v0);
scanf_s(&v25);
strcpy(&v5, &v25, 50);
v18 = v5;
v5 = v34;
v6 = v26 + 2;
v17 = v7;
v7 = v33;
v8 = v27 + 2;
v16 = v9;
v9 = v32;
v10 = v28 + 2;
v15 = v11;
v11 = v31;
v1 = 0;
v12 = v29 + 2;
v14 = v13;
v13 = v30;
do
{
    v4[v1] = *(&v5 + v1) ^ 0xCC;
    ++v1;
}
while ( v1 <= 19 );
    v2 = 0;
while ( v4[v2] == *(_DWORD *)((char *)&v19 + v2 * 4) )
{
    ++v2;
    if ( v2 > 18 )
        return 0;
}
printf("Error!", v4[0]);
```

## 分析
flag一共20位，可以以**flag{ABCDEFGHIJKLMNO}**输入为例

简单来分析就是**f**和**}**交换，**l**那个位置变成了**ord(g)+2** 
**a**和**N**交换以此类推，**g**那个位置变成**ord(A)+2**
最后变成
```
7D 69 4E 43 4C 45 4A 47  47 45 46 44 48 42 4B 7B  }iNCLEJGGEFDHBK{
4D 61 4F 66                                       MaOf
```
然后和**0XCC**异或，最后和字母表验证，字母表扣出来是
```
B1 00 00 00 A4 00 00 00  B5 00 00 00 87 00 00 00
AD 00 00 00 AD 00 00 00  93 00 00 00 B9 00 00 00
BF 00 00 00 BF 00 00 00  93 00 00 00 FD 00 00 00
FC 00 00 00 B8 00 00 00  FF 00 00 00 B7 00 00 00
F9 00 00 00 B8 00 00 00  ED 00 00 00 A4 00 00 00
flag{ABCDE
FGHIJKLMN}
```
写个脚本就解决了
