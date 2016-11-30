#

## 前年的题
开始在linux没法运行，然后看了前年的wp <br>
在ida中打开strings窗口，查找flag类似的字符串，然后定位代码<br>
发现是很长的一段，就是矩阵的乘法。<br>

## dump出矩阵
本来想一个一个扣，结果实在太多了，就把ida中的伪都复制出来，一部分改动了一下，然后用正则表达式解析
```Python
for i in range(1, 23):
    patt_str = ('\d+\*m' + str(i) + '\n')
    pt = re.compile(patt_str)
    mk_str = re.findall(pt, fp_buf)
    for k in range(len(mk_str)):
        pt = re.compile('\d+')
        fuz_martix[k][i-1] = int(re.search(pt, mk_str[k]).group(0))
```
这样基本就dump出了矩阵的参数，其中注意的是**fuz_martix**定义应该是
```Python
fuz_martix =  [[0 for col in range(22)] for row in range(22)]
```
其他形式可能有问题

## 解矩阵
用numpy来解
```Python
import numpy as np
a = np.array(fuz_martix)
b = np.array(result)
x = solve(a, b)
print(x)
```
解出来发现顺序不对，开始ida改变量名没有注意，转一下就好了

