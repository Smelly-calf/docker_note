# Docker compose

https://docs.docker.com/compose/

Docker compose 是一个定义和运行多容器应用程序的工具。

通过Compose，您可以使用YAML文件来配置你的应用程序服务。然后，使用一个命令，就可以从配置中创建并启动所有服务。

Compose可在所有环境中工作：生产，登台，开发，测试以及CI工作流。说白了，compose 可以实现自动化。

使用Compose基本上是一个三步过程：
- 编写Dockerfile 定义应用程序的环境，以便在任何地方复制应用程序环境。
- 编写docker-compose.yml定义组成你应用程序的服务们，以便可以在隔离环境一起运行。
- 运行 docker-compose up，Compose 启动并运行整个应用程序。

`docker-compose.yml` 例子：
```
version: "3.8"
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/code
      - logvolume01:/var/log
    links:
      - redis
  redis:
    image: redis
volumes:
  logvolume01: {}
```

Compose具有用于管理应用程序整个生命周期的命令：
- 启动，停止和重建服务
- 查看正在运行的服务的状态
- 流运行服务的日志输出
- 对服务运行一次性命令

## Install Compose
On Linux CentOS8
