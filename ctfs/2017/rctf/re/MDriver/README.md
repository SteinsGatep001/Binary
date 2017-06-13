
## Preface

环境折腾了好久

## Easy Env

实际上有个很简单的工具，看了大佬的博客[fuzzysecurity kernel exp](http://www.fuzzysecurity.com/tutorials/expDev/14.html)

## where is flag

查找内存字符串
```cmd
s -sa fffff804`39ce0000 L1D100
.....
fffff804`39ce5d02  "E#H"
fffff804`39ce5d9d  "E#H"
fffff804`39ce5e01  "E#H"
fffff804`39ce5e82  "E#H"
fffff804`39ce5ed6  "E#H"
fffff804`39ce5f42  "E#H"
fffff804`39ce5f9b  "E#H"
fffff804`39ce601f  "E#H"
fffff804`39ce638e  "1\ the flag is A_simple_Inline_h"
fffff804`39ce63ae  "ook_Drv"
fffff804`39ce6416  "1\@"
```
