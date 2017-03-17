## Vuln
很简单的栈溢出
不过又是canary的问题

## bypass
之前绕过是直接leak的，这里是出题人写的socket，读不到leak出来的canary值

所以采用单字节爆破的方式


