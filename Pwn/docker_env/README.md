## 说明

利用docker来构建pwn环境比较安全和方便，不过也有一些不方便的地方。比如printf格式化输出的问题，端口映射之后不能打印字符串等。。

>参考0ctf2016 pwn的工程

## 配置
创建了两个Dockerfile

### Dockerfile.base
```
sudo docker build --network=host -t ubpwn:base .
```
生成一个基础镜像，主要下载一些要用的固件和服务。需要指定网络模式host，否则不能联网下载。

### Dockerfile
```
sudo docker build --network=host -t bxs:pwn1 .
```
生成最终的镜像可以直接通过以下命令运行
```
sudo docker run -p 2333:2333 bxs:pwn1
```
注意端口映射

### 导出镜像
```
docker save -o pwndocker.tar pwn1:pwn1
```

### 导入镜像
```
sudo docker load --input pwndocker.tar
```
