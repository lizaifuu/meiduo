#!/usr/bin/env python3

print('hello')

# 修改数据库的图片url
# update tb_sku set default_image_url=replace(default_image_url, 'http://127.0.0.1:8888', 'http://176.140.7.173:8888')
#
# update tb_goods set desc_detail=replace(desc_detail, 'http://127.0.0.1:8888', 'http://176.140.7.173:8888')

# create database meiduo default charset=utf8;


# 在docker上配置主从mysql
# docker run --name mysql-slave -e MYSQL_ROOT_PASSWORD=mysql -d --network=host -v /home/tarena/mysql-slave/data:/var/lib/mysql -v /home/tarena/mysql-slave/mysql.conf.d:/etc/mysql/mysql.conf.d mysql:5.7.26


# mysql -uroot -pmysql -h127.0.0.1 --port=8306

