## Tips
1.因为程序里alarm限制时间60s
handle SIGALRM print nopass 可以用来把alarm关掉(实际上我也没法gdb调试, 不知道为什么)
2.堆溢出比较复杂(理解就花了好久,现在也还不是特别清晰), 画图来理解稍微好点

## 结构体

```
 sh_st           struc ; (sizeof=0x18, mappedto_1) ; XREF: .bss:stru_6016C0/r
00000000 flag            dq ?                    ; XREF: new_sh+AA/w
00000008 size            dq ?                    ; XREF: new_sh+B5/w
00000010 name_ptr        dq ?                    ; XREF: new_sh+BC/w
00000018 sh_st           ends
```

## 漏洞点
get_name(sh_st->name_ptr, length); // 这里length也是输入的，但是这里没有对length检查，所以在new创建的size如果小于这个，就会发生堆溢出

## 利用原理
small chunk // large chunk 在某相邻的chunk free之后, 该chunk对前后的chunk检查, 如果为free, 就进行向前或向后何必, 并且把检查到的free chunk从bins双链表中删除

由linux堆的结构可以知道，如果创建了chunk1，再创建chunk2(这里可以说是name_ptr指向的地方)，chunk的头部信息首先是

```
0x00 pre chunk size
0x08 chunk size |N|M|P| P=0 : pre chunk free
0x10 fd
0x18 bk
```
其中主要P表示前一堆块是否被使用

这里把P覆盖成0的话，就会使程序错误的执行ulink, 而且程序错误的认为name_ptr_0 是free chunk 即可以认为name_ptr_0指向了bin里的一个项
```c
/* Take a chunk off a bin list */
#define unlink(AV, P, BK, FD)
{                             
    FD = P->fd;	//P == &chunk1					          
    BK = P->bk;								   
    if (__builtin_expect (FD->bk != P || BK->fd != P, 0))		    
      malloc_printerr (check_action, "corrupted double-linked list", P, AV); 
    else
    {								    
        FD->bk = BK;				
        BK->fd = FD;                //需要注意这里 就是把free chunk从双链表删除
      
        //large chunk do something
        //...
    }
}
```
P->fd->bk = P->bk; 

P->fd = addr-0x18 , P->bk = value 时 

P->fd->bk = P->bk 相当于修改*((addr-0x18)+0x18) 为 value


## 流程
主要流程是:

1.创建三个chunk chunk[0~3]

2.edit(chunk0) 构造chunk0为free chunk并且覆盖下chunk1的头部

3.然后释放chunk1 触发unlink 修改0x6016d0(name_ptr 0的地址)为前面的一地址(0x6016b8)

4.调用edit(chunk0) 对0x6016b8那一段空间的值更改, 而且刚好能够更改到name_ptr 0的地址(更改为got表中free的地址)

5.调用list(0)就可以leak出真实的free地址, 然后计算真实的system函数地址, 绕过ASLR

6.再次调用edit(0) 对got表中free更改, 更改为4中获得的system函数地址, 那么之后只要调用free, 就相当于调用system

7.只要之前把chunk3那边写有"/bin/sh"相关字符串的free掉, 就能执行system了

8.第一次搞orz 照着别人的自己理解的改(抄)了下

### 计算system函数地址
利用libc库中的free函数地址

objdump -T lib.so.6 | grep system 

本机的so库: lib_sys_addr =  0x0000000000046590

            lib_free_addr = 0x0000000000082d00
            
提供的so库: lib_sys_addr =  0x0000000000046640

            lib_free_addr = 0x0000000000082df0
            
system_addr = free_addr - lib_free_addr + lib_sys_addr


### 遇到的坑
1.data_0  = 'p'*(first_size-0x20)   这里伪造的时候填充的数据需要减去头部信息, 而不是new时候的大小

2.size_1  = p64(second_size + 0x10) 这里要注意第二个块的大小是加上头部的pre chunk size和自身chunk size 并没有fd和bk

3.读取leak出的free地址

样例用的是zio 而我自己用pwn

这个真是坑惨了, 搞了好几个小时(不知道为什么没法调试), 结果就是读取的时候没有把地址转换对orz(我好菜啊)

我用的转换方法好笨orz 其实最简单的是用zio的l64

return l64(io.read(16).decode('hex'))
```
recv_addr = p.read(8 * 2) #这里注意对读取的地址进行适当的转换
ret_addr = ''
for i in range(8):
    ret_addr += recv_addr[2*i+1] + recv_addr[2*i]
print type(recv_addr), len(recv_addr), recv_addr
print type(ret_addr), len(ret_addr), ret_addr
return int(ret_addr[::-1], 16)
```

## Reference
[Linex 堆](http://tyrande000.how/2016/02/20/linux%E4%B8%8B%E7%9A%84%E5%A0%86%E7%AE%A1%E7%90%86/)

[linux 堆 上](https://jiji262.github.io/wooyun_articles/drops/Linux%E5%A0%86%E7%AE%A1%E7%90%86%E5%AE%9E%E7%8E%B0%E5%8E%9F%E7%90%86%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0%20(%E4%B8%8A%E5%8D%8A%E9%83%A8).html)

[linux 堆 下](https://jiji262.github.io/wooyun_articles/drops/Linux%E5%A0%86%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86%E6%B7%B1%E5%85%A5%E5%88%86%E6%9E%90(%E4%B8%8B%E5%8D%8A%E9%83%A8).html)

[linux 堆 unlink利用](http://tyrande000.how/2016/03/21/linux%E5%A0%86%E6%BA%A2%E5%87%BA%E5%AE%9E%E4%BE%8B%E5%88%86%E6%9E%90/)
强网杯”网络安全挑战赛WriteUp
