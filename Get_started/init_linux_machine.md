
一、查看系统信息
```
cat /etc/redhat-release //查看内核系统
cat /proc/version //查看Linux系统
uname -a
df -h //查看磁盘，如96C
top //内存
```

二、useradd wangqian
```
useradd -d /data4/home/wangqian -m -s "/bin/bash" wangqian

useradd -d /data1/home/$user -m -s "/bin/bash" $user 
chmod a+w /etc/sudoers
vim /etc/sudoers
给用户wangqian添加sudo权限
chmod a-w /etc/sudoers
```

三、安装 Docker 

在线安装：https://docs.docker.com/engine/install/centos/
```log
Error: Package: 3:docker-ce-20.10.6-3.el7.x86_64 (docker-ce-stable)
           Requires: libseccomp >= 2.3
           Available: libseccomp-2.1.1-2.el7.i686 (CentOS)
               libseccomp = 2.1.1-2.el7
```

离线安装：https://docs.docker.com/engine/install/binaries/#install-static-binaries

| CentOS 7 | CentOS 8 |
| --- | --- |
| docker17.12| docker19|

https://docs.docker.com/engine/install/linux-postinstall/

创建 docker group
```
groupadd docker
usermod -aG docker $USER
id $USER
```
启动：sudo dockerd &

rm -f /var/run/docker.pid

配置 deamon.json
```
vim /etc/docker/daemon.json

{
  "insecure-registries" : ["myregistrydomain.com:5000"]
}
```
重启
```
ps -ef | grep docker | awk '{print $2}' | sed -n '2p' | xargs kill -9
sudo dockerd &
```

四、安装 MySQL

参考 `practice/docker_mysql.md`

五、安装 go

https://golang.org/doc/install

六、git拉服务代码

启动服务

访问：
```
# 1.GET
curl http://testapi.easy-olap.jd.local/v1/clusters 

# 2.GET 某集群id账号列表
curl http://testapi.easy-olap.jd.local/v1/clusters/id

# 3.PUT 批量修改账号配额
curl -v -X PUT -d '{"accountIds":[],"profile":[{"name":"queries","value":100}]}' http://testapi.easy-olap.jd.local/v1/accounts/profile

带cookie的put请求
curl -H 'Cookie: ' -v -X PUT -d '{"accountIds":[],"profile":[{"name":"queries","value":100}]}' http://testapi.easy-olap.jd.local/v1/accounts/profile
```

七、备份：
```
rsync -avzP --exclude 'liyang830' --exclude 'songenjie' --exclude 'liyang830.zip' /data1/home  root@10.203.24.118:/data1/home
```
