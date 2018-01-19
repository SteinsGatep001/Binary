![](pwn_pwn.jpg)

## 工具
IDA+pwndbg+pwntools+...

### IDA
先祭上神器

### pwndbg
这个比peda好用一点。推荐。

- **stack** 100 查看栈信息
- **heap** -h 查看堆(需要更全的heap插件可以看[libheap](https://github.com/cloudburst/libheap)，不过这个基本够了)

#### gdb自定义hook(这里自定制用，其实pwngdbg自带就完全足够了)
```asm
define hook-stop
>info registers
>x/24wx $esp
>x/2i $eip
>end
```

### pwntools
具体网上一堆教程如：[pwntools使用](http://www.cnblogs.com/pcat/p/5451780.html)，这里就是个人整理一点

```Python
p = process('./pwnfun') # 挂载进程
elf = ELF('./pwnfun') # 看到的结果就和checksec一样
p.interactive() # 弹shell
context.log_level = 'debug' # 挂进程之后显示各种调试信息
```
- **DynELF**这个用来leak十分好用，不过leak格式比较难写，有点迷
- elf.got['puts'] 这个少用，也有点迷，用ROPgadget(见下文)代替比较好

#### dbg

关闭ptrace使得能够attach
```
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope
```
程序中调用调试
```
gdb_code='b *0x4009F2\nb *0x400A6D\nb *0x400778\nb*0x400944\n'
gdb.attach(proc.pidof(io)[0],gdb_code)
```

### checksec（pwntools中也有)

```
CANARY : 覆盖返回地址基本不可利用
FORTIFY : 一种安全机制
NX : 堆栈不可执行
PIE : 攻击时需要泄露地址
RELRO : Partial: 不可修改strtab
Full : 程序装载时填充got表
```

### ropper

之前一直用`ROPgadget`，不过后来发现还是`ropper`更好

### metsploit
```bash
msfconsole
msf >
show payloads: 显示所有渗透模块
use linux/x64/exec: 使用linux x64 模块
set cmd /bin/sh
generate -t py -b "/x00":产生shellcode /xXX的形式
```

### redare2(要用的话再积累 IDA更加方便)
```gdb
aaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze len bytes of instructions for references (aar)
[x] Analyze function calls (aac)
s sym.main:运行到main处
pdf:打印汇编
odd [strings]: 给参数来运行程序
dc: 运行程序
db: 下断点
dr: 查看所有寄存器信息
VV: 查看调用关系视图
afvn [name] [name]: 重命名，类似ida的n

echo disass main | gdb ./[program] 利用管道来调试
"\41\xffABCD".encode('hex'
set disassembly-flavor intel 设置为x86汇编显示
```


## Complie
- gcc
```bash
-fno-stack-protector// 去除栈保护 如 gcc -m32 -g -fno-stack-protector -z execstack -o vuln vuln.c
```
- nasm
```bash
nasm -f elf -o vlun.o vuln.asm //编译
ld -m elf_i386 -s -o vuln vuln.o vuln.o //链接
./vuln 运行
```

## 一些姿势

### 连接
```bash
ssh user@192.168.47.143 用来连接目标主机
scp user@192.168.47.143 [filename] [dir]
scp -P2222 col@pwnable.kr:/home/passcode
```
### 程序加载追踪
```bash
ltrace
strace
```
### 测试
主要看socat用法
```bash
socat tcp-listen:12345 exec:./stack_overflow 把程序放到本机运行
socat tcp-listen:22333,reuseaddr,fork system:./pwnme 保持程序一直执行
nc 127.0.0.1 12345 本地测试连接
```

### 调试`libc`源码

基本步骤不难<br>

#### 1. 安装`libc`的调试库
````bash
# x86_64
sudo apt-get install libc6-dbg
# 32bit 可以安装下面的
sudo apt-get install libc6:i386
sudo apt-get install libc6-dbg:i386
```

#### 2. 把源码下下来`sudo apt install glibc-source`

#### 3. 进入`gdb`，指定源码目录（比如malloc）
```bash
pwndbg> dir /usr/src/glibc/glibc-2.26/malloc
Source directories searched: /usr/src/glibc/glibc-2.26/malloc:/usr/src/glibc/glibc-2.26:$cdir:$cwd
──────────────────────────────────────────────────────────────────────[ SOURCE (CODE) ]───────────────────────────────────────────────────────────────────────
   3052 #define MAYBE_INIT_TCACHE()
   3053 #endif
   3054
   3055 void *
   3056 __libc_malloc (size_t bytes)
 ► 3057 {
   3058   mstate ar_ptr;
   3059   void *victim;
   3060
   3061   void *(*hook) (size_t, const void *)
   3062     = atomic_forced_read (__malloc_hook);
```

### Docker

写好Dockerfile之后
```
# 构建image，注意网络配置
sudo docker build --network=host -t csaw:warmup .
# 运行 注意端口映射
sudo docker run -p 8000:8000 csaw:warmup
```
具体`docker`相关的配置在`docker_env`里面

### Centos 相关

centos可能默认开了防火墙 所以端口都是关闭的 但是关闭防火墙又不太好，所以开放对应端口就好了

- 通过命令开启允许对外访问的网络端口(这里是23333)：
```bash
/sbin/iptables -I INPUT -p tcp --dport 23333 -j ACCEPT
/etc/rc.d/init.d/iptables save
/etc/rc.d/init.d/iptables restart
/etc/init.d/iptables status// 查看端口是否开放
```
### 关闭alarm

alarm比较烦，不方便调试

handle SIGALRM print nopass 可以用来把alarm关掉(实际上我也没法gdb调试, 不知道为什么)

### 加载信息
```bash
info proc map 查看各个库加载信息然后寻找 "/bin/sh" 字符串
strings: 查看文件中可见字符串
strings -a -t x /lib32/libc.so.6 | grep "/bin/sh"
objdump -d stack7 | grep "ret" 可以用来查找ret指令
objdump -x [filename] 打印头文件信息以及区段信息
objdump -T libc.so | grep gets
```
### 查找gadgets
```bash
ROPgadget --binary level4 --only "pop|ret"
ROPgadget --binary libc.so.6 --only "pop|ret" | grep rdi
objdump -d ./level5
__libc_csu_init这个函数里找 ROP
objdump -d -j.plt pwn | grep write 查找write函数地址
```
## Konwledge
QAQ

#### 覆盖`x86_64 ret libc`
执行call操作时栈内已经存放了传递的变量，call将当前地址压入栈中，作为返回地址，然后执行jmp到指定函数位置。构造call system时可以利用这个先存放一个地址，然后跳转。
#### ROP
基础技能了，不过自己经常是会忘，都要照着汇编来看参数传递顺序≧ ﹏ ≦

附上文章[uaf_io find system](http://uaf.io/exploitation/misc/2016/04/02/Finding-Functions.html)
#### uaf
pwnable

#### double free
主要就是堆堆的大小要十分的清楚
#### unlink
一般都是结合其他的一些漏洞一起用

#### off-by-one
孤独的1byte

#### shrink
就是改变堆大小进行进一步利用

#### `IO_FILE`
这个是文件流相关的利用，著名的有`house of orange`

### 一些坑

#### 关于DynELF
有一定的成功率，不过如果网速或者服务器不过关，这个方法并不是很好，dl-resolve相对易成功一点。baidu杯那个不知道是不是这个原因QAQ
#### 其他的坑
to be continued

## resources

### [pwnable](http://pwnable.kr/play.php)
主要linux elf为主 比较适合开拓思路和入门，做过一点，不过因为懒，有点荒废了

配上[writeup-riskgray](http://rickgray.me/2015/07/24/toddler-s-bottle-writeup-pwnable-kr.html)食用更佳
### [io](http://io.netgarage.org/)
还没来得及看，主要是有arm的

### [LiveOverFlow](https://www.youtube.com/channel/UClcE-kVhqyiHCcjYwcpfj9w)
youtube有相关视频 从他的视频学了不少
### [CTF writeup](https://github.com/ctfs)
各种writeup (大多国外)，感觉国内各ctf都参照了很多国外的比赛
### CTFer-bin

- [muhe](http://o0xmuhe.me/)
- [hackfun](https://www.hackfun.org/)
- [Icemakr](http://0byjwzsf.me/) LCTF2016 pwn出题大大
- [Zing](http://l-team.org/)
- [tang](http://bigtang.org/)
- [uaf](http://uaf.io/) 国外一位，各种ctf wp都有他的身影

### [resource recommand](http://www.pentest.guru/index.php/2016/01/28/best-books-tutorials-and-courses-to-learn-about-exploit-development/)
各种资源，看了晕
### [DEF CON](https://www.defcon.org/#)
知名hacker团队
### [tisiphone](https://tisiphone.net/)
推送多 有心得体会系列文章可以看看
