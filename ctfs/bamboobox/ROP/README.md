## Description
nc 140.113.209.24 10001

## orz
就是一个盲的，需要构造下

```C
open("/home/ctf/flag", "rb")
read(3, buf, 0x40)
write(1, buf, 0x40)
```

### option
```Assembly
0.	int 0x80
	pop ebp
	pop edi
	pop esi
	pop ebx
============================
1.	pop ebx
	pop ebp
	xor eax,eax
============================
2.	sub ecx,eax
	pop ebp
============================
3.	mov edx,eax
	pop ebx
============================
4.	pop ecx
	pop eax
============================
5.	mov (esp),edx
============================
6.	pop edx
	pop ecx
	pop edx
============================
7.	add ecx,eax
	pop ebx
============================
8.	add eax,0x2
============================
9.	push esp
	push ebp
============================
10.	push 0x68732f6e
	push 0x69622f2f
============================
11.	push 0x67616c66
	push 0x2f2f6674
	push 0x632f2f65
	push 0x6d6f682f
============================
12.	push 1
	push 2
============================
13.	push eax
============================
```
