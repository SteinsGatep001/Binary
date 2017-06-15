## vlun

开始看的晕了，长度有限制，max_len是21，但是后来想想第一个read name的时候可以更改，但是后面strlen(name)，长度又有限制<br>

### tips
strlen是以0判断结尾的，而程序通过read读取<br>
所以输入
```Python
'a'+chr(0)+'aaaaaa'
```
strlen返回长度为1，利用这个绕过长度限制造成栈溢出
