###reverse03:
闲着无聊 做了学校的ctf平台的一题（之前遗留了）
先uxp脱壳 然后拖进ida
主要代码如下

    falgDug = 0;
    inUser = 0;                                   // [bp-14h] 开始依次 48, 52, 49, 55, 53, 49, 51, 48, 48, 49, 51, 50
    v_13h = 0;
    v_Fh = 0;
    v22 = 0;
    v23 = 0;
    inPass = 0;
    v13 = 0;
    v14 = 0;
    v15 = 0;
    v16 = 0;
    v17 = 0;
    v18 = 0;
    printf("输入用户名:");
    scanf("%15s", &inUser);
    printf("\n");
    printf("输入密码:");
    scanf("%25s", &inPass);
    iU = strlen(&inUser);
    for ( i = 0; i < iU; ++i )
    {
    if ( *(&inUser + i) < '0' || *(&inUser + i) > '9' )
    {
      printf("用户名必须为数字");
      goto LABEL_13;
    }
    }
    v9 = GetTickCount();
    v5 = &loc_401052;
    IsOver = 0x40;
    do
    {                                             // check int
    if ( !IsOver )
      break;                                    // 检测int3断点防止调试
    getInt3 = *(_BYTE *)v5 == 0xCCu;
    v5 = (char *)v5 + 1;
    --IsOver;
    }
    while ( !getInt3 );
    if ( getInt3 )
    falgDug = 1;
    isInt = (GetTickCount() - v9) / 0x3E8 > 1;    // 判断时间，防止调试
    produceAlph1(falgDug, (int)&inUser, isInt);
    produceAlph2((char *)&v_13h + 3);
    produceAlph3((char *)&v_Fh + 3);
    checkPassword(&inPass);
    LABEL_13:
    system("pause");
    return 0;
***
看到解密的数组列表
    alph1='onhtxdsqvpzcrefjigklfzbapvdqsxzrcefimlku'
    alph2='zscbmdvholblzftuhsxsbchanrcdqjvqfinotcbu'
    alph3='pzywrvdcbqeuafsxgmlitnkopvdqsxtdnapcuwys'
    这里是在ida里算偏移算出来的
    username:041751300132
    对应位置为
    bp-[h]  14  13  12  11  10  0f  0e  0d  0c  0b  0a  09
    //      48, 52, 49, 55  53, 49, 51, 48  48, 49, 51, 50
***
    注意到
    produceAlph1中有个检测int3断点的程序，防止OD调试
    v9 = GetTickCount();
    v5 = &loc_401052;
    IsOver = 0x40;
    do
    {                                             // check int
    if ( !IsOver )
      break;                                    // 检测int3断点防止调试
    getInt3 = *(_BYTE *)v5 == 0xCCu;
    v5 = (char *)v5 + 1;
    --IsOver;
    }
    while ( !getInt3 );
    if ( getInt3 )
    falgDug = 1;
***
    ###IDA伪指令解析错误:
    怎么写脚本调都不对，问了学长，flag对了，但是伪C代码逻辑有改地方不对
    这个地方：
    f_8 = *((_BYTE *)&aIdaq64_exe[5 * (isDbg + 2 * (unsigned __int8)isFsd) + 2] + *(_BYTE *)pThis);
    反过去汇编才发现ida F5解析错了 应该是：
    *((_BYTE *)&aIdaq64_exe[2 * 5 * (isDbg + 2 * (unsigned __int8)isFsd)]才对吧
***
    .text:00401420 var_4           = dword ptr -4
    .text:00401420
    .text:00401420                 push    ebp
    .text:00401421                 mov     ebp, esp
    .text:00401423                 push    ecx
    .text:00401424                 push    ebx
    .text:00401425                 push    esi
    .text:00401426                 mov     esi, ecx
    .text:00401428                 mov     [ebp+var_4], 0  ; var_4 = 0
    .text:0040142F                 mov     cl, 1
    .text:00401431                 mov     eax, large fs:'0'
    .text:00401437                 mov     eax, [eax+68h]  ; eax += fs:'0'
    .text:0040143A                 mov     [ebp+var_4], eax
    .text:0040143D                 test    byte ptr [ebp+var_4], 'p'
    .text:00401441                 mov     eax, 0
    .text:00401446                 movzx   ebx, cl         ; if (var_4 == 'p') ebx = 1
    .text:00401446                                         ; else     ebx = 0
    .text:00401449                 cmovnz  ebx, eax
    .text:0040144C                 call    ds:IsDebuggerPresent
    .text:00401452                 neg     eax             ; if (IsDebuggerPresent) eax = 1
    .text:00401452                                         ; else eax = 0
    .text:00401454                 movzx   ecx, bl         ; 设isFsd = bl
    .text:00401457                 sbb     eax, eax
    .text:00401459                 neg     eax             ; 设isDbg = eax
    .text:0040145B                 lea     eax, [eax+ecx*2] ; eax = isDbg + 2*isFsd
    .text:0040145E                 lea     ecx, [eax+eax*4] ; ecx = 5*(eaxL) = 5*(isDbg + 2*isFsd)
    .text:00401461                 movsx   eax, byte ptr [esi]
    .text:00401464                 movzx   eax, byte ptr [eax+ecx*2+4021A0h] ; 2*ecx = 2*5*(isDbg + 2*isFsd) = 10*(isDbg + 2*isFsd)
    .text:0040146C                 mov     f_8, al         ; 当 isDbg=0 isFsd=1 该值为 10*2-20
    .text:0040146C                                         ; 和ad3_1 = 0
    .text:0040146C                                         ; ad3_2 = 1
    .text:0040146C                                         ; ad3 = 5*(ad3_1 + 2 * ad3_2 + 2) = 20 一致
    .text:00401471                 movsx   eax, byte ptr [esi+1]
    .text:00401475                 movzx   eax, byte ptr [eax+ecx*2+4021A0h]
    .text:0040147D                 mov     f_9, al
    .text:00401482                 movsx   eax, byte ptr [esi+2]
    .text:00401486                 movzx   eax, byte ptr [eax+ecx*2+4021A0h]
    .text:0040148E                 mov     f_10, al
    .text:00401493                 movsx   eax, byte ptr [esi+3]
    .text:00401497                 pop     esi
    .text:00401498                 pop     ebx
    .text:00401499                 movzx   eax, byte ptr [eax+ecx*2+4021A0h]
    .text:004014A1                 mov     f_11, al
    .text:004014A6                 mov     esp, ebp
    .text:004014A8                 pop     ebp
    .text:004014A9                 retn
    .text:004014A9 produceAlph3    endp

    (
    neg r 指令的结果是设置Carry Flag, 也就是借位的标志位. 因为neg r的操作语义是0 - r, 零减去任何非零的数,都会产生"借位"的. 当然这里r寄存器中的值也被改掉了,不过没关系, 反正它都要被稍后的指令再改掉的.
    sbb r, r 指令设置r为零或者-1. 因为语义为用一个值去减掉它自身, 结果当然是零啰. 但是,这样做会把carry flag一起给减掉的, 该指令的公式是
    r – r – CF –>  r 

    为零(ZF=1) CMOVZ AX, BX
    CMOVZ r32, r/m32 CMOVZ EAX, EB
    )
***
####推广 题目来自:http://219.219.60.244/challenges.php 普普通通的逆向
