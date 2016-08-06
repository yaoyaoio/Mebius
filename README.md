
###引言：Mebius是根据梦比优斯奥特曼的英文名命名的


Mebius是基于saltapi使用django开发的资产管理平台

支持centos6.x,ubuntu等系统的资产收集
更新资产目前不支持磁盘更新，等待完善
支持批量命令,基于web的salt认证
支持日志审计（添加资产的还没写完）
支持用户管理
支持部门管理

此代码仅供学习参考,生产目前可能会有bug

一切问题都可以联系我进行处理QQ:22102107



大概截图：

![](http://i.imgur.com/tuINEhq.jpg)
![](http://i.imgur.com/fcTlKpD.jpg)
![](http://i.imgur.com/jOl0QN4.jpg)
![](http://i.imgur.com/7n8RkXC.jpg)
![](http://i.imgur.com/2uCLCXa.jpg)
![](http://i.imgur.com/EeGqCVE.jpg)
![](http://i.imgur.com/ZJrK2m2.jpg)
![](http://i.imgur.com/7VVgN3P.jpg)
![](http://i.imgur.com/g8AA9fd.jpg)
![](http://i.imgur.com/wbla4PB.jpg)




1.部署saltapi平台

	#yum install salt-api -y
	#useradd saltapi
	#passwd saltapi
	#修改master配置
	#vim /etc/salt/master
	配置如下
	default_include: master.d/*.conf
	file_roots:
	  base:
	    - /salt/states
	  dev:
	    - /salt/dev
	  prod:
	    - /salt/prod
	# cd /etc/salt/
	# mkdir master.d/
	# cd master.d/
	创建两个文件内容和名字如下
	# cat api.conf 
	rest_cherrypy:
	  host: 0.0.0.0
	  port: 8080
	  debug: true
	  disable_ssl: true
	# cat eauch.conf 
	external_auth:
	  pam:
	    saltapi:
	      - .*
	      - '@wheel'
	      - '@runner'
	#/etc/init.d/salt-api start
	#创建自定义grains目录和放入相应获取信息的脚本
	/salt/states/_grains/
	total 24
	-rw-r--r-- 1 root root  826 Jul 26 10:07 cpuinfo.py
	-rw-r--r-- 1 root root 1018 Jul 26 22:15 diskinfo.py
	-rw-r--r-- 1 root root  873 Jul 28 17:29 dmide.py
	-rw-r--r-- 1 root root 2251 Jul 26 10:07 nicinfo.py
	-rw-r--r-- 1 root root  423 Jul 30 19:56 osinfo.py
	-rw-r--r-- 1 root root 1960 Jul 26 22:13 raminfo.py
	#重启服务
	# /etc/init.d/salt-master restart
	

2.将salt密码放入Mebius配置里
	#打开Mebius工程的setting的文件
	里面最低有写入salt的密码


3.python的依赖包省略,缺啥pip啥就可以


之后运行
