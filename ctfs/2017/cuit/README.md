

## Pwn

### Escape From Jail

来啊py交易啊~<br>
nc 54.222.255.223 50000

### Just Drink Lemon Water

我是一颗山中修炼千年的大柠檬，擅长制作柠檬水。你想来试一试么？<br>
nc 54.222.255.223 50001

### Tiny FileShare

share file with us!

http://game.sycsec.com/download/pwn200_ok.9a2055bed81cf667

nc 54.222.255.223 50002


### Notebook
l3m0n 的小本本上好多不可描述的秘密...<br>
try to exploit && get it !

### Life Crowdfunding

真正的粉丝发起了一个活动，快来参加吧！<br>
nc 119.29.87.226 50004


## Re

程序段是要解密后才能看的，main:0x804848F下断点
```assembly
73 8D F2 4C C7 D4 7B F7  18 32 71 0D CF DC 67 4F
7F 0B 6D 00 00 00 00 00  00 00 00 00 00 00 00 00
```
分析知是循环移位
