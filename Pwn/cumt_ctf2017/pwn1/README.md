## 描述
你为什么这么熟练啊，你到底溢出了几次啊（出自白色相簿2 冬马和纱（笑））

## vuln
checksec发现开了栈保护
题目中有两个read，均可可以溢出。

## 思路
第一次read读到canary，然后第二次把第一次获得的canary拼接到payload中，绕过canary并且造成溢出
程序里给了getflag函数，直接把返回地址覆盖成getflag地址，然后读取即可

