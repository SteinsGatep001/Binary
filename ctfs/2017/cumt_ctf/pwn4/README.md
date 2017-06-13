
## Preface

出这个的时候开始考虑的是fastbin dup，后面检查发现也可以用unlink，正式比赛之前又改成了fastbin dup。。<br>
可能有其他解法，orz，大佬求指教<br>


### dfffff

这个是可以有unlink的，大小没限制到fastbin

### pwn4

正式的题目，限制不能超过fastbin大小

## 笑

可以参考https://github.com/shellphish/how2heap/blob/master/fastbin_dup_into_stack.c
学习一下fastbin attack(自己找个简单的例子更好)<br>

exp给了
