问题：使用 xxx/go:1.14 镜像创建并启动一个容器，在容器中通过 localhost 连接 mysql server 失败

解决：
1. 配置 `bind-address` 至改为 `0.0.0.0`，配置文件在`/usr/local/etc/my.cnf`
2. 修改用户密码
    ```
    update mysql.user set authentication_string=password('root123') where user='root';
    ```
3. 授权所有主机：
    ```
    grant all privileges on *.* to 'root'@'%'  IDENTIFIED BY 'root' with grant option;
    ```

参考文档：
[Networking features in Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/networking/#there-is-no-docker0-bridge-on-macos#i-want-to-connect-from-a-container-to-a-service-on-the-host)


docker 安装 myql

-/data2/mysql/my.cnf
```
!includedir /etc/mysql/conf.d/
!includedir /etc/mysql/mysql.conf.d/
```

-data2/mysql/mysql.conf.d/mysqld.cnf
```
[client]
default-character-set=utf8

[mysql]
default-character-set=utf8

[mysqld]
init_connect='SET collation_connection=utf8_unicode_ci'
init_connect='SET NAMES utf8'
character-set-server=utf8
collation-server=utf8_unicode_ci
skip-character-set-client-handshake
skip-name-resolve
```

启动：
```
docker rm --force adminmysql
docker run --restart=always --privileged=true -d -v /data2/mysql/data:/var/lib/mysql -v /data2/mysql/conf.d:/etc/mysql/conf.d -v /data2/mysql/mysql.conf.d:/etc/mysql/mysql.conf.d -v /data2/mysql/my.cnf:/etc/mysql/my.cnf -p 3306:3306 --name adminmysql -e MYSQL_ROOT_PASSWORD=root123 -d mysql:5.7.19
```


goadmin：
```
docker run -it -p 3306:3306 --name goadmin-database-test -e MYSQL_ROOT_PASSWORD=root123 -d mysql:5.7.19
docker exec -it goadmin-database-test mysql -uroot -root123
```

`docker cp /data3/goadmin_test/goadmin/db/ goadmin-database-test:/` 复制文件到容器

执行： `use adminserver;  source /db/admin.sql` 导入数据

```
cd /data3/${jobName}_${gitSourceBranch}/go-admin
make serve
```

配置代理访问 `http://ip:9033/admin/`

登录后点击左侧「菜单」添加我们自己数据库路由: `/info/$key`
