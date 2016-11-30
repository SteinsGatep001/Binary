#

## 拨洋葱
### 1. 头部
前面就首先验证了**}**才进入第一个函数的解析
```asm
.data:0000000000601576 ; ---------------------------------------------------------------------------
.data:0000000000601576
.data:0000000000601576 loc_601576:                             ; CODE XREF: step1_xor_125+76j
.data:0000000000601576 mov     edx, [rbp+var_8]
.data:0000000000601579 mov     eax, [rbp+var_4]
.data:000000000060157C lea     ecx, [rdx+rax]
.data:000000000060157F mov     eax, [rbp+var_4]
.data:0000000000601582 movsxd  rdx, eax
.data:0000000000601585 mov     rax, [rbp+var_28]
.data:0000000000601589 add     rax, rdx
.data:000000000060158C movzx   eax, byte ptr [rax]              ; flag[i]
.data:000000000060158F movsx   eax, al
.data:0000000000601592 xor     ecx, eax                         ; flag[i] ^ 0x10
.data:0000000000601594 mov     edx, ecx
.data:0000000000601596 mov     eax, [rbp+var_4]
.data:0000000000601599 cdqe
.data:000000000060159B movzx   eax, byte ptr [rbp+rax+alph]     ; alph[i] 72 66 75 6F 7F
.data:00000000006015A0 movsx   eax, al
.data:00000000006015A3 cmp     edx, eax
.data:00000000006015A5 jz      short loc_6015AE
.data:00000000006015A7 mov     eax, 0
.data:00000000006015AC jmp     short locret_601614
.data:00000000006015AE ; ---------------------------------------------------------------------------
```
异或之后就是flag前5个了
### 2. 前几个字符
首先把flag每4位的拆开
```C++
flag_off5 = flag + 5;
for ( i = 0; (signed int)i <= 3; ++i )
{
    split_str[2 * i] = *(_BYTE *)((signed int)i + flag_off5) & 0xF;
    split_str[2 * i + 1] = *(_BYTE *)((signed int)i + flag_off5) >> 4;
}
```
接下来生成0~ff的字典序列
```C++
for ( i = 0; (signed int)i <= 0xFF; ++i )
    alpt_ff[i] = i;
```
接下来先是从flag里面取前四个字符(hctf)，然后对前面生成的表进行变换
```C++
tmp_offset = 4;
tmp_k = 0;
for ( i = 0; (signed int)i <= 0xFF; ++i )
{
    v3 = ((signed int)(alpt_ff[i] + tmp_k + flag_off0[i % tmp_offset]) >> 31) >> 24;
    tmp_k = (unsigned __int8)(v3 + alpt_ff[i] + tmp_k + flag_off0[i % tmp_offset]) - v3;
    tmp_chnumber = (unsigned __int8)alpt_ff[i];
    alpt_ff[i] = alpt_ff[tmp_k];
    alpt_ff[tmp_k] = tmp_chnumber;
}
```
接着
```C++
now_len = 8
i = 0;
tmp_k = 0;
for ( j = 0; j < now_len; ++j )
{
    i = (unsigned __int8)(((unsigned int)((signed int)(i + 1) >> 31) >> 24) + i + 1)
      - ((unsigned int)((signed int)(i + 1) >> 31) >> 24);
    v4 = (unsigned int)((signed int)(tmp_k + (unsigned __int8)alpt_ff[i]) >> 31) >> 24;
    tmp_k = (unsigned __int8)(v4 + tmp_k + alpt_ff[i]) - v4;
    tmp_chnumber = (unsigned __int8)alpt_ff[i];
    alpt_ff[i] = alpt_ff[tmp_k];
    alpt_ff[tmp_k] = tmp_chnumber;
    v16 = (unsigned __int8)alpt_ff[(unsigned __int8)(alpt_ff[i] + alpt_ff[tmp_k])];
    split_str[j] ^= v16;
}
// 调试可以发现 v16[]是固定的
v16[] = {59 0c 98 96 23 29 0E 8F};
```
其实搞了半天就是类rc4，只要把上面的v16扣出来，和最后的**5D 09 90 90 26 2F 01 8A**异或，最后比较
```
5D 09 90 90 26 2F 01 8A
loc_60131B:
mov     eax, [rbp+var_4]
cdqe
movzx   edx, [rbp+rax+split_str]
mov     eax, [rbp+var_4]
cdqe
movzx   eax, byte ptr [rbp+rax+var_40]
cmp     dl, al
jz      short loc_60133D
```
所以解决的方法就是先把那边的数据都异或，然后拼起来，转换成对应ascii
### 3. base64/32 变异
```
.data:000000000060165A ; ---------------------------------------------------------------------------
.data:000000000060165A
.data:000000000060165A loc_60165A:                             
.data:000000000060165A mov     rax, [rbp-8]
.data:000000000060165E lea     rdx, [rax+1]
.data:0000000000601662 mov     [rbp-8], rdx
.data:0000000000601666 mov     rdx, [rbp-38h]
.data:000000000060166A movzx   edx, byte ptr [rdx]
.data:000000000060166D sar     dl, 2                    
.data:0000000000601670 add     edx, 30h                                 ; flag[k]>>2+0x30
.data:0000000000601673 mov     [rax], dl
.data:0000000000601675 mov     rax, [rbp-8]
.data:0000000000601679 lea     rdx, [rax+1]
.data:000000000060167D mov     [rbp-8], rdx                             
.data:0000000000601681 mov     rdx, [rbp-38h]
.data:0000000000601685 movzx   edx, byte ptr [rdx]
.data:0000000000601688 movsx   edx, dl
.data:000000000060168B shl     edx, 4                                   ; flag[k]<<4
.data:000000000060168E mov     ecx, edx
.data:0000000000601690 and     ecx, 30h                                 ; flag[k]<<4&0x30
.data:0000000000601693 mov     rdx, [rbp-38h]
.data:0000000000601697 add     rdx, 1
.data:000000000060169B movzx   edx, byte ptr [rdx]
.data:000000000060169E sar     dl, 4                                    ; flag[k+1]>>4
.data:00000000006016A1 add     edx, ecx                                 ; flag[k+1] + (flag[k]<<4)&0x30
.data:00000000006016A3 add     edx, 30h                                 ; (flag[k+1] + (flag[k]<<4)&0x30) + 0x30
.data:00000000006016A6 mov     [rax], dl
.data:00000000006016A8 mov     rax, [rbp-8]
.data:00000000006016AC lea     rdx, [rax+1]
.data:00000000006016B0 mov     [rbp-8], rdx
.data:00000000006016B4 mov     rdx, [rbp-38h]
.data:00000000006016B8 add     rdx, 1
.data:00000000006016BC movzx   edx, byte ptr [rdx]
.data:00000000006016BF movsx   edx, dl
.data:00000000006016C2 shl     edx, 2                                   ; flag[k+1]<<2
.data:00000000006016C5 mov     ecx, edx
.data:00000000006016C7 and     ecx, 3Ch                                 ; flag[k+1]<<2 & 0x3c
.data:00000000006016CA mov     rdx, [rbp-38h]
.data:00000000006016CE add     rdx, 2
.data:00000000006016D2 movzx   edx, byte ptr [rdx]                      ; flag[k+2]
.data:00000000006016D5 sar     dl, 6                                    ; flag[k+2]>>6
.data:00000000006016D8 add     edx, ecx                                 ; flag[k+2]>>6 + (flag[k+1]<<2) & 0x3c
.data:00000000006016DA add     edx, 30h                                 ; (flag[k+2]>>6 + (flag[k+1]<<2) & 0x3c) + 0x30
.data:00000000006016DD mov     [rax], dl
.data:00000000006016DF mov     rax, [rbp-8]
.data:00000000006016E3 lea     rdx, [rax+1]
.data:00000000006016E7 mov     [rbp-8], rdx
.data:00000000006016EB mov     rdx, [rbp-38h]
.data:00000000006016EF add     rdx, 2                                   ; flag[k+2]
.data:00000000006016F3 movzx   edx, byte ptr [rdx]
.data:00000000006016F6 and     edx, 3Fh
.data:00000000006016F9 add     edx, 30h                                 ; flag[k+2]&0x3f + 0x30
.data:00000000006016FC mov     [rax], dl
.data:00000000006016FE add     qword ptr [rbp-38h], 3
.data:0000000000601703 add     dword ptr [rbp-0Ch], 1
.data:0000000000601707
.data:0000000000601707 loc_601707:                             ; CODE XREF: .data:0000000000601655j
.data:0000000000601707 cmp     dword ptr [rbp-0Ch], 1
.data:000000000060170B jle     loc_60165A
.data:0000000000601711 mov     dword ptr [rbp-0Ch], 0
.data:0000000000601718 jmp     short loc_60173D
.data:000000000060171A ; ---------------------------------------------------------------------------

```
总结起来就是3->4的变换
```
flag[k]>>2+0x30
(flag[k+1] + (flag[k]<<4)&0x30) + 0x30
(flag[k+2]>>6 + (flag[k+1]<<2) & 0x3c) + 0x30
flag[k+2]&0x3f + 0x30
```
最后的比较序列是 **40 56 35 63 4A 46 3D 4F**，一共是8个，解出来就OK
### 4. 简单的位置交换
```
.data:0000000000601091 ; ---------------------------------------------------------------------------
.data:0000000000601091
.data:0000000000601091 loc_601091:                             ; CODE XREF: .data:00000000006010F0j
.data:0000000000601091 mov     eax, [rbp-4]
.data:0000000000601094 movsxd  rdx, eax
.data:0000000000601097 mov     rax, [rbp-28h]
.data:000000000060109B add     rax, rdx
.data:000000000060109E movzx   eax, byte ptr [rax]
.data:00000000006010A1 and     eax, 0Fh                         ; flag[t]&0x0F
.data:00000000006010A4 mov     [rbp-9], al
.data:00000000006010A7 mov     eax, [rbp-4]
.data:00000000006010AA movsxd  rdx, eax
.data:00000000006010AD mov     rax, [rbp-28h]
.data:00000000006010B1 add     rax, rdx
.data:00000000006010B4 movzx   eax, byte ptr [rax]
.data:00000000006010B7 sar     al, 4                            ; flag[t]>>4
.data:00000000006010BA mov     [rbp-0Ah], al
.data:00000000006010BD shl     byte ptr [rbp-9], 4
.data:00000000006010C1 movzx   eax, byte ptr [rbp-0Ah]
.data:00000000006010C5 or      [rbp-9], al
.data:00000000006010C8 movzx   eax, byte ptr [rbp-9]            ; flag[t]&0x0F<<4 | flag[t]>>4 实际上就是low4和high4交换了一下
.data:00000000006010CC xor     eax, 11h                         ; 
.data:00000000006010CF mov     [rbp-0Ah], al
.data:00000000006010D2 mov     eax, [rbp-4]
.data:00000000006010D5 cdqe
.data:00000000006010D7 movzx   eax, byte ptr [rbp+rax-20h]
.data:00000000006010DC cmp     al, [rbp-0Ah]

```
扣出来就是 **12 77 E4 34 45 E4**，和0x11异或之后把low4和high4交换，接着就转ascii了
### 5. 出题人的仁慈
做到这里其实已经感觉比较烦了，以为还来个什么md5变形什么的，结果毕竟是正常的逆向

直接比较最后的所有字符了，直接扣出来就行


## Summary
1. 首先要对各个算法的变形清楚，多看一些常见加密算法的程序，这次不是很熟悉各个程序，花了比较久的时间

2. 最好先定位异或和比较这些地方，方便找对应的表值和理解程序逻辑


