#项目名称 -- 学海网

####项目环境

此项目环境是python2.7.12，建议使用虚拟环境，需要的包在`requirements.txt` 中，在终端中`cd xxxx` 'xxxx' 是此项目的目录，src的同级目录，运行命令`pip install　-r requirements.txt` 安装相关的包，

####配置文件

安装nginx：`sudo apt-get install nginx` 运行`ifconfig` 查看IP地址(inet后的数字)。 安装uwsgi：`sudo apt-get install uwsgi` 安装mysql: `sudo apt-get insatll mysql-server` 。建议安装navicat for mysql能更好的管理mysql。在 etc/mysql/mysql.conf.d/mysql.cnf中将端口改好。运行 `mysql` 在mysql中运行`GRANT ALL PRIVILEGES ON *.* TO '用户名'@'%' IDENTIFIED BY '密码' WITH GRANT OPTION;` 与`FLUSH PRIVILEGES;` 。　

配置文件在conf文件夹中，拷贝`uc_nginx.conf` 到 `/etc/nginx/conf.d` 目录。

启动uwsgi: `uwsgi --http :8000 --module ruan.wsgi` ruan.wsgi为本项目的wsgi的文件目录。

####关于目录的修改

在conf文件夹的uc_nginx.conf文件中，你会看到`server_name 192.168.22.129 www.xuehai.com; #substitute your machine's IP address or FQDN` 这一行，请将这一行中的IP地址更改为你的主机IP地址，后面的域名更改为你的域名。

在`# 指向django的media目录`　前的路径更改为你的项目存放的media目录

在`# 指向django的static目录`　前的路径更改为你的静态文件目录

在conf文件夹中的uwsgi.ini配置文件中

在`chdir           = /home/aiyane/aiyane/myWork/src` 这一行的路径中更改为你的项目存放路径

在`virtualenv = /home/aiyane/.virtualenvs/ruan` 这一行更改为你的虚拟环境的路径

运行命令`python manage.py collecstatic` 配置所有静态文件

####启动

cd 到　conf文件同级目录，运行命令`uwsgi -i uwsgi.ini` 启动服务器即可．
