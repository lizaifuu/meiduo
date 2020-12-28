
"""
    Django实现前后端分离的商城项目
    python & html & css & javascript & vue
"""
需求功能

项目架构
    项目采用前后端分离的应用模式
    前端使用Vue.js
    后端使用Django REST framework


在docker上配置主从mysql
docker run --name mysql-slave -e MYSQL_ROOT_PASSWORD=mysql -d --network=host -v /home/tarena/mysql-slave/data:/var/lib/mysql -v /home/tarena/mysql-slave/mysql.conf.d:/etc/mysql/mysql.conf.d mysql:5.7.26

开启docker 中的mysql
mysql -uroot -pmysql -h127.0.0.1 --port=8306

将主机mysql所有的数据导出到一个sql文件中
mysqldump -uroot -p123456 --all-databases --lock-all-tables > ~/.master_db.sql

将导出的数据库写入到docker中的数据库中
mysql -uroot -pmysql -h127.0.0.1 --port=8306 < ./master_db.sql

创建用于从服务器的账号
GRANT REPLICATION SLAVE ON *.* TO 'slave'@'%' identified by 'slave';

刷新权限
FLUSH PRIVILEGES;

查看主机中mysql的二进制文件位置状态
SHOW MASTER STATUS;

在从服务器中配置
change master to master_host='127.0.0.1', master_user='slave', master_password='slave', master_log_file='mysql-bin.000001', master_log_pos=590;

在从服务器中开始
start slave

查看从服务器的状态
show slave status \G;

配置成功
Slave_IO_Running: Yes
Slave_SQL_Running: Yes

如果是用sudo apt-get install nginx安装nginx的时候,nginx的配置文件在/etc/nginx
如果是用用源码安装的话 nginx的配置文件在 /usr/local/nginx


        
# meiduo
# meiduo
