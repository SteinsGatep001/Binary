#

## ǰ�����
��ʼ��linuxû�����У�Ȼ����ǰ���wp <br>
��ida�д�strings���ڣ�����flag���Ƶ��ַ�����Ȼ��λ����<br>
�����Ǻܳ���һ�Σ����Ǿ���ĳ˷���<br>

## dump������
������һ��һ���ۣ����ʵ��̫���ˣ��Ͱ�ida�е�α�����Ƴ�����һ���ָĶ���һ�£�Ȼ����������ʽ����
```
for i in range(1, 23):
    patt_str = ('\d+\*m' + str(i) + '\n')
    pt = re.compile(patt_str)
    mk_str = re.findall(pt, fp_buf)
    for k in range(len(mk_str)):
        pt = re.compile('\d+')
        fuz_martix[k][i-1] = int(re.search(pt, mk_str[k]).group(0))
```
����������dump���˾���Ĳ���������ע�����**fuz_martix**����Ӧ����
```
fuz_martix =  [[0 for col in range(22)] for row in range(22)]
```
������ʽ����������

## �����
��numpy����
```
import numpy as np
a = np.array(fuz_martix)
b = np.array(result)
x = solve(a, b)
print(x)

```
���������˳�򲻶ԣ���ʼida�ı�����û��ע�⣬תһ�¾ͺ���

