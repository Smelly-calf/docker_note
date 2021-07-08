使用 Docker+Jenkins实现Go项目的持续集成

整体的实现思路：

`推送代码至Git服务器` => 

`触发Jenkins服务器配置的Git Web Hooks` => `从Git服务器中pull或clone代码` => `将代码编译成二进制可执行文件` => `构建docker镜像` => `上传docker镜像至镜像仓库` => 

`从Jenkins服务器进入远程应用服务器` => `从docker镜像仓库中拉取镜像` => `停止并删除该项目正在运行的docker容器` => `使用该新镜像构建并启动docker容器` => `删除其他旧版本镜像` => `完成`

 