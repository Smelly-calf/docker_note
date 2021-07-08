# 添加一个组
groupadd olap
# 定义组管理员
gpasswd -A <user_name> <group_name>
# 设定组密码
gpasswd <group_name>
# 创建用户并/home创建同名的文件夹
useradd –g <group_name> -m <user_name>
# 修改用户加入某个组
usermod –g <group_name> <user_name>
# 修改用户密码
passwd <username>
# 给用户添加 sudo 权限
a) 切换至root账户，为sudo文件增加写权限，默认是读权限
chmod u+w /etc/sudoers


b) 打开文件vim /etc/suduers，在root ALL=(ALL) ALL这一行下面添加
daiyu ALL=(ALL) ALL
c) 再次取消sudo文件的写权限
chmod u-w /etc/sudoers


# 查看组成员
cat /etc/group | grep <group_name>

# 删除组成员
gpasswd -d <user> <group_name>
# 取消组密码
gpasswd -r olap
# 删除组
groupdel olap
# 添加组成员
gpasswd -a <user> <group_name>


# 修改用户主目录
1. 修改 /etc/passwd 
2. usermod -d /data2/home/wangqian -u $uid wangqian