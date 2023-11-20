# docker
## 各个参数作用
```
  -d, --detach 后台运行容器，并输出容器ID
  -e, --env list 设置环境变量，该变量可以在容器内使用
  -h, --hostname string 指定容器的hostname
  -i, --interactive 以交互模式运行容器，通常与-t同时使用
  -l, --label list 给容器添加标签
  --name string 设置容器名称，否则会自动命名
  --network string 将容器加入指定网络
  -p, --publish list 设置容器映射端口 hostPort:containerPort
  -P,--publish-all 将容器设置的所有exposed端口进行随机映射
  --restart string 容器重启策略，默认为不重启
    on-failure[:max-retries]：在容器非正常退出时重启，可以设置重启次数。
    unless-stopped：总是重启，除非使用stop停止容器
    always：总是重启
  --rm 容器退出时则自动删除容器
  -t, --tty 分配一个伪终端
  -u, --user string 运行用户或者UID
  -v, --volume list 数据挂载
  -w, --workdir string 容器的工作目录
  --privileged 给容器特权
```

# 安装各种镜像
## Nginx
docker pull nginx
1. 制作挂载卷 
mkdir -p /mount/docker/nginx/html
mkdir -p /mount/docker/nginx/logs
mkdir -p /mount/docker/nginx/conf/
**运行容器**  docker run -d -p 80:80 --name nginx nginx 
2. 拷贝配置文件
```sh
docker cp nginx:/etc/nginx/nginx.conf /mount/docker/nginx/conf/nginx.conf
docker cp nginx:/etc/nginx/conf.d /mount/docker/nginx/conf.d
docker cp nginx:/usr/share/nginx/html /mount/docker/nginx
```
**删除原先容器**
docker rm nginx
3. 启动容器

docker run \
-p 80:80 \
--name nginx \
-v /mount/docker/nginx/conf/nginx.conf:/etc/nginx/nginx.conf \
-v /mount/docker/nginx/conf.d:/etc/nginx/conf.d \
-v /mount/docker/nginx/logs:/var/log/nginx \
-v /mount/docker/nginx/html:/usr/share/nginx/html \
-d nginx:latest
**乌班图安装**
```sh
#安装
apt-get install nginx
# 查看版本
nginx -v
service nginx start
```
## TOMCAT
1. 安装步骤
1.1、搜索tomcat镜像
$ docker search tomcat
通过上述命令查找tomcat镜像,选择Apache的tomcat，一般搜索到的结果，Apache tomcat是排在第一个的。而后可以进行安装。

2. 安装tomcat镜像
$ docker pull tomcat
1.3、查看安装的tomcat镜像
$ docker images
该命令回列出已经安装的tomcat镜像。

3. 启动tomcat容器
$ docker run --name tomcat-test -d -p 8080:8080 tomcat
4. 解决404
启动之后浏览器输入 192.168.44.130:8080 发现页面输出404，这就有点纳闷了，在其他人的博客中找到了解决方法。
```c
#进入 tomcat 容器查看文件

# 进入tomcat,0be1774e1e5e为容器ID
docker exec -it 0be1774e1e5e /bin/bash
#删除webapps文件夹，将webapps.dist文件夹改成webapps

rm -rf webapps/

mv webapps.dist/ webapps/
exit
再次访问 192.168.44.130:8080 ，页面访问成功。
```
5. 容器文件映射到本地目录（挂载）
制作挂载卷 
mkdir -p /mount/docker/tomcat

拷贝容器内 tomcat 配置文件和日志到本地准备映射

docker cp tomcat-test:/usr/local/tomcat/conf /mount/docker/tomcat/conf
docker cp tomcat-test:/usr/local/tomcat/logs /mount/docker/tomcat/logs
docker cp tomcat-test:/usr/local/tomcat/webapps /mount/docker/tomcat/webapps
停止tomcat，并删除容器

docker stop tomcat-test
docker rm tomcat-test
创建并运行tomcat容器

docker run -d -p 8080:8080 --name tomcat -v /mount/docker/tomcat/webapps:/usr/local/tomcat/webapps -v /mount/docker/tomcat/conf:/usr/local/tomcat/conf -v /mount/docker/tomcat/logs:/usr/local/tomcat/logs tomcat
此时如果浏览器访问404， 则需要再次进入 tomcat 容器：

docker exec -it tomcat-test1 /bin/bash
删除 webapps 文件夹，并重命名 webapps.dist 为 webapps:

rm -r webapps
mv webapps.dist webapps

## OpenResty
**一、拉取镜像**
docker pull openresty/openresty
**二、启动**
docker run --name openresty -p 80:80 -d openresty/openresty

**三、复制配置文件**
1、创建宿主机目录
mkdir -p /mount/docker/openresty/conf
mkdir /mount/docker/openresty/conf.d
mkdir /mount/docker/openresty/logs
mkdir /mount/docker/openresty/lua
2、拷贝容器中nginx配置文件到宿主机目录
```cmd
#nginx配置文件

docker cp openresty:/usr/local/openresty/nginx/conf/nginx.conf /mount/docker/openresty/conf/
docker cp openresty:/usr/local/openresty/nginx/html /mount/docker/openresty/
docker cp openresty:/etc/nginx/conf.d /mount/docker/openresty/
# 拷贝lua库
docker cp openresty:/usr/local/openresty/lualib /mount/docker/openresty/
```
**四、删除容器，启动新容器**

docker rm -f openresty

docker run -p 80:80 \
--name openresty  \
-v /mount/docker/openresty/conf/nginx.conf:/usr/local/openresty/nginx/conf/nginx.conf \
-v /etc/localtime:/etc/localtime \
-v /mount/docker/openresty/conf.d:/etc/nginx/conf.d \
-v /mount/docker/openresty/html:/usr/local/openresty/nginx/html \
-v /mount/docker/openresty/logs:/usr/local/openresty/nginx/logs \
-v /mount/docker/openresty/lualib:/usr/local/openresty/lualib \
-v /mount/docker/openresty/lua/:/usr/local/openresty/nginx/lua \
-d openresty/openresty

**五、测试lua模块**
1、新建item.lua
在/usr/local/openresty/lua/新建item.lua

-- 返回假数据，这里的ngx.say()函数，就是写数据到Response中
ngx.say('{"id":"10001","name":"SALSA"}')
1
2
2、修改配置文件nginx.conf

http {
    # 隐藏版本号
	server_tokens off;
    include       mime.types;
    default_type  application/octet-stream;
	underscores_in_headers on;#表示如果header name中包含下划线，则不忽略

    sendfile        on;
    #keepalive_timeout  0;
    keepalive_timeout  65;

    gzip  on;

    #include /etc/nginx/conf.d/*.conf;
	#lua 模块
	lua_package_path "/usr/local/openresty/lualib/?.lua;;";
	#c模块     
	lua_package_cpath "/usr/local/openresty/lualib/?.so;;";  

    server {
        listen       80;
        server_name  127.0.0.1;
		
		location /api/item {
            # 默认的响应类型
            default_type application/json;
            # 响应结果有lua/item.lua文件来决定
            content_by_lua_file lua/item.lua;
         
        }
		
        location / {
            root   html;
            index  index.html index.htm;
        }

   }
}
## 安装redis
1. 拉去 docker pull redis 
2. 制作挂在目录（/mount/docker/redis）
```s
mkdir -p /mount/docker/redis/conf

mkdir -p /mount/docker/redis/data
```


3. 下载redis.conf文件
wget http://download.redis.io/redis-stable/redis.conf
4. 调整配置文件
```
bind 127.0.0.1 # 这行要注释掉，解除本地连接限制
protected-mode no # 默认yes，如果设置为yes，则只允许在本机的回环连接，其他机器无法连接。
daemonize no # 默认no 为不守护进程模式，docker部署不需要改为yes，docker run -d本身就是后台启动，不然会冲突
requirepass 123456 # 设置密码
appendonly yes # 持久化
```
4.. 运行
```s
docker run --name redis \
-p 6379:6379 \
-v /mount/docker/redis/data:/data \
-v /mount/docker/redis/conf/redis.conf:/etc/redis/redis.conf \
-d redis redis-server /etc/redis/redis.conf
```
**闪退解决**
1. 赋予挂载目录（权限 chmod -R 777 文件名）
2. aemonize no

## elasticsearch

###  docker-compose安装
```yml
version: '3'
services:
  elasticsearch:
    image: elasticsearch:8.11.0
    container_name: elasticsearch
    restart: always
#     privileged: true
    environment:
      - discovery.type=single-node #以单一节点模式启动
      - ES_JAVA_OPTS=-Xms512m -Xmx512m #设置使用jvm内存大小
      - cluster.name=elasticsearch #设置集群名称为elasticsearch
      - node.name=elastic01 #设置节点名称为elasticsearch
      - network.host=0.0.0.0 # 网络访问限制，设置所有都可以访问
      - http.host=0.0.0.0
      - http.cors.allow-origin="*" # 表示支持所有域名
      - bootstrap.memory_lock=true # 内存交换的选项，官网建议为true
      - xpack.security.enabled=false # 修改安全配置 关闭 证书校验
      - xpack.security.http.ssl.enabled=false
      - xpack.security.transport.ssl.enabled=false
      - ELASTIC_PASSWORD=123456   #密码
    volumes:
      # - ./es/config/elasticsearch.ymldocker:/usr/share/elasticsearch/config/elasticsearch.yml 
      # - ./es/data:/usr/share/elasticsearch/data
      - ./es/plugins:/usr/share/elasticsearch/plugins 
      # - ./es/logs:/user/share/elasticsearch/logs
    ports:
      - 9200:9200
      - 9300:9300
    networks:
      - elasticsearch  
  kibana:
    image: kibana:8.11.0
    container_name: kibana
    restart: always
    depends_on:
      - elasticsearch #kibana在elasticsearch启动之后再启动
    environment:
      # - "elasticsearch.hosts=http://elasticsearch:9200" #设置访问elasticsearch的地址
      # - "ELASTICSEARCH_USERNAME=elastic"    
      # - "ELASTICSEARCH_PASSWORD=123456"    #elastic密码
      - "I18N_LOCALE=zh-CN"                 #中文
    ports:
      - 5601:5601
    networks:
        - elasticsearch  
networks:
    elasticsearch:
        driver: bridge

```      
此时，在浏览器输入地址访问：http://192.168.150.101:5601，即可看到结果

docker 
```s
docker run -p 9200:9200 -p 9300:9300 --name elasticsearch \
-e  "discovery.type=single-node" \
-e ES_JAVA_OPTS="-Xms512m -Xmx1g" \
-v  /mount/docker/elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
-v  /mount/docker/elasticsearch/data:/usr/share/elasticsearch/data \
-v  /mount/docker/elasticsearch/plugins:/usr/share/elasticsearch/plugins \
-d elasticsearch:8.6.1
```
## gogs
```s
docker pull gogs/gogs

mkdir -p /mount/docker/gogs

docker run --name=gogs -d  -p 10022:22 -p 10880:3000 -v /mount/docker/gogs:/data gogs/gogs
```




## rabbitmq
```shell
docker run \
 -e RABBITMQ_DEFAULT_USER=admin \
 -e RABBITMQ_DEFAULT_PASS=admin \
 -v mq-plugins:/plugins \
 --name mq \
 --hostname mq \
 -p 15672:15672 \
 -p 5672:5672 \
 -d \
 rabbitmq:management
```

```s
docker pull rabbitmq:management

mkdir -p /mount/docker/rabbitmq/{data,conf,log}

chmod -R 777 /mount/docker/rabbitmq


docker run --privileged=true \
-d -p 5672:5672 -p 15672:15672 \
--restart=always --hostname=rabbitmqhost -e RABBITMQ_DEFAULT_VHOST=my_vhost -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin \
rabbitmq:management

```




7、开启端口

firewall-cmd --zone=public --add-port=5672/tcp --permanent

firewall-cmd --zone=public --add-port=15672/tcp --permanent

firewall-cmd --reload
### 开启web管理端
1、进入容器，

docker exec -it rabbitmq bash
2、开启web管理端

rabbitmq-plugins enable rabbitmq_management
3、创建用户

默认账户密码都是 guest

默认用户guest访问报错User can only log in via localhost解决方案

第一种
只能本机通过localhost方式访问了，一般不安装图形界面，所以这个基本不会选择

第二种

用admin/admin账号密码登录，创建

Add a user

Virtual Hosts

Set permission，点击用户名，设置权限

 第三种：

1.首先进入容器 docker exec -it rabbitmq /bin/bash

2.创建用户 rabbitmqctl add_user admin1 admin1

3.给用户授权角色 rabbitmqctl set_user_tags admin1 administrator

4.给用户添加权限 rabbitmqctl set_permissions -p / admin1 ".*" ".*" ".*"
4、可以使用浏览器打开web管理端：http://Server-IP:15672.

## mysql
```s
docker pull mysql

mkdir -p /mount/docker/mysql/{data,conf,logs}
vim /mount/docker/mysql/conf/my.cnf
```
my.cnf
添加配置文件
```ini
[mysqld]
#Mysql服务的唯一编号 每个mysql服务Id需唯一
server-id=0

#服务端口号 默认3306
port=3306

#mysql安装根目录（default /usr）
#basedir=/usr/local/mysql

#mysql数据文件所在位置
datadir=/var/lib/mysql

#pid
pid-file=/var/run/mysqld/mysqld.pid

#设置socke文件所在目录
socket=/var/lib/mysql/mysql.sock

#设置临时目录
#tmpdir=/tmp

# 用户
user=mysql

# 允许访问的IP网段
bind-address=0.0.0.0

# 跳过密码登录
#skip-grant-tables

#主要用于MyISAM存储引擎,如果多台服务器连接一个数据库则建议注释下面内容
#skip-external-locking

#只能用IP地址检查客户端的登录，不用主机名
#skip_name_resolve=1

#事务隔离级别，默认为可重复读，mysql默认可重复读级别（此级别下可能参数很多间隙锁，影响性能）
#transaction_isolation=READ-COMMITTED

#数据库默认字符集,主流字符集支持一些特殊表情符号（特殊表情符占用4个字节）
character-set-server=utf8mb4

#数据库字符集对应一些排序等规则，注意要和character-set-server对应
collation-server=utf8mb4_general_ci

#设置client连接mysql时的字符集,防止乱码
init_connect='SET NAMES utf8mb4'

#是否对sql语句大小写敏感，1表示不敏感
lower_case_table_names=1

#最大连接数
max_connections=400

#最大错误连接数
max_connect_errors=1000

#TIMESTAMP如果没有显示声明NOT NULL，允许NULL值
explicit_defaults_for_timestamp=true

#SQL数据包发送的大小，如果有BLOB对象建议修改成1G
max_allowed_packet=128M

#MySQL连接闲置超过一定时间后(单位：秒)将会被强行关闭
#MySQL默认的wait_timeout  值为8个小时, interactive_timeout参数需要同时配置才能生效
interactive_timeout=1800
wait_timeout=1800

#内部内存临时表的最大值 ，设置成128M。
#比如大数据量的group by ,order by时可能用到临时表，
#超过了这个值将写入磁盘，系统IO压力增大
tmp_table_size=134217728
max_heap_table_size=134217728

#禁用mysql的缓存查询结果集功能
#后期根据业务情况测试决定是否开启
#大部分情况下关闭下面两项
#query_cache_size = 0
#query_cache_type = 0
 
#数据库错误日志文件
#log-error=/var/log/mysqld.log

#慢查询sql日志设置
#slow_query_log=1
#slow_query_log_file=/var/log/mysqld_slow.log

#检查未使用到索引的sql
log_queries_not_using_indexes=1

#针对log_queries_not_using_indexes开启后，记录慢sql的频次、每分钟记录的条数
log_throttle_queries_not_using_indexes=5

#作为从库时生效,从库复制中如何有慢sql也将被记录
log_slow_slave_statements=1

#慢查询执行的秒数，必须达到此值可被记录
long_query_time=8

#检索的行数必须达到此值才可被记为慢查询
min_examined_row_limit=100

#mysql binlog日志文件保存的过期时间，过期后自动删除
#expire_logs_days=5
binlog_expire_logs_seconds=604800

```
```s
docker run -itd -p 3306:3306 \
--name mysql \
-v /mount/docker/mysql/conf/my.cnf:/etc/my.cnf \
-v /mount/docker/mysql/data:/var/lib/mysql \
-v /mount/docker/mysql/log:/var/log/mysql \
--privileged=true \
--restart=always \
-e MYSQL_ROOT_PASSWORD=root \
-d mysql:latest
```
docker run -itd -p 3306:3306 \
--name mysql \
--privileged=true \
--restart=always \
-e MYSQL_ROOT_PASSWORD=root \
-d mysql:latest
## nacos
```sql
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_info   */
/******************************************/
CREATE TABLE `config_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(255) DEFAULT NULL,
  `content` longtext NOT NULL COMMENT 'content',
  `md5` varchar(32) DEFAULT NULL COMMENT 'md5',
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '修改时间',
  `src_user` text COMMENT 'source user',
  `src_ip` varchar(20) DEFAULT NULL COMMENT 'source ip',
  `app_name` varchar(128) DEFAULT NULL,
  `tenant_id` varchar(128) DEFAULT '' COMMENT '租户字段',
  `c_desc` varchar(256) DEFAULT NULL,
  `c_use` varchar(64) DEFAULT NULL,
  `effect` varchar(64) DEFAULT NULL,
  `type` varchar(64) DEFAULT NULL,
  `c_schema` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_configinfo_datagrouptenant` (`data_id`,`group_id`,`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='config_info';
 
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_info_aggr   */
/******************************************/
CREATE TABLE `config_info_aggr` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(255) NOT NULL COMMENT 'group_id',
  `datum_id` varchar(255) NOT NULL COMMENT 'datum_id',
  `content` longtext NOT NULL COMMENT '内容',
  `gmt_modified` datetime NOT NULL COMMENT '修改时间',
  `app_name` varchar(128) DEFAULT NULL,
  `tenant_id` varchar(128) DEFAULT '' COMMENT '租户字段',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_configinfoaggr_datagrouptenantdatum` (`data_id`,`group_id`,`tenant_id`,`datum_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='增加租户字段';
 
 
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_info_beta   */
/******************************************/
CREATE TABLE `config_info_beta` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(128) NOT NULL COMMENT 'group_id',
  `app_name` varchar(128) DEFAULT NULL COMMENT 'app_name',
  `content` longtext NOT NULL COMMENT 'content',
  `beta_ips` varchar(1024) DEFAULT NULL COMMENT 'betaIps',
  `md5` varchar(32) DEFAULT NULL COMMENT 'md5',
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '修改时间',
  `src_user` text COMMENT 'source user',
  `src_ip` varchar(20) DEFAULT NULL COMMENT 'source ip',
  `tenant_id` varchar(128) DEFAULT '' COMMENT '租户字段',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_configinfobeta_datagrouptenant` (`data_id`,`group_id`,`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='config_info_beta';
 
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_info_tag   */
/******************************************/
CREATE TABLE `config_info_tag` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(128) NOT NULL COMMENT 'group_id',
  `tenant_id` varchar(128) DEFAULT '' COMMENT 'tenant_id',
  `tag_id` varchar(128) NOT NULL COMMENT 'tag_id',
  `app_name` varchar(128) DEFAULT NULL COMMENT 'app_name',
  `content` longtext NOT NULL COMMENT 'content',
  `md5` varchar(32) DEFAULT NULL COMMENT 'md5',
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '修改时间',
  `src_user` text COMMENT 'source user',
  `src_ip` varchar(20) DEFAULT NULL COMMENT 'source ip',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_configinfotag_datagrouptenanttag` (`data_id`,`group_id`,`tenant_id`,`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='config_info_tag';
 
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_tags_relation   */
/******************************************/
CREATE TABLE `config_tags_relation` (
  `id` bigint(20) NOT NULL COMMENT 'id',
  `tag_name` varchar(128) NOT NULL COMMENT 'tag_name',
  `tag_type` varchar(64) DEFAULT NULL COMMENT 'tag_type',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(128) NOT NULL COMMENT 'group_id',
  `tenant_id` varchar(128) DEFAULT '' COMMENT 'tenant_id',
  `nid` bigint(20) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`nid`),
  UNIQUE KEY `uk_configtagrelation_configidtag` (`id`,`tag_name`,`tag_type`),
  KEY `idx_tenant_id` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='config_tag_relation';
 
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = group_capacity   */
/******************************************/
CREATE TABLE `group_capacity` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `group_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'Group ID，空字符表示整个集群',
  `quota` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '配额，0表示使用默认值',
  `usage` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '使用量',
  `max_size` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '单个配置大小上限，单位为字节，0表示使用默认值',
  `max_aggr_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '聚合子配置最大个数，，0表示使用默认值',
  `max_aggr_size` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '单个聚合数据的子配置大小上限，单位为字节，0表示使用默认值',
  `max_history_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '最大变更历史数量',
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='集群、各Group容量信息表';
 
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = his_config_info   */
/******************************************/
CREATE TABLE `his_config_info` (
  `id` bigint(64) unsigned NOT NULL,
  `nid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `data_id` varchar(255) NOT NULL,
  `group_id` varchar(128) NOT NULL,
  `app_name` varchar(128) DEFAULT NULL COMMENT 'app_name',
  `content` longtext NOT NULL,
  `md5` varchar(32) DEFAULT NULL,
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00',
  `src_user` text,
  `src_ip` varchar(20) DEFAULT NULL,
  `op_type` char(10) DEFAULT NULL,
  `tenant_id` varchar(128) DEFAULT '' COMMENT '租户字段',
  PRIMARY KEY (`nid`),
  KEY `idx_gmt_create` (`gmt_create`),
  KEY `idx_gmt_modified` (`gmt_modified`),
  KEY `idx_did` (`data_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='多租户改造';
 
 
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = tenant_capacity   */
/******************************************/
CREATE TABLE `tenant_capacity` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `tenant_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'Tenant ID',
  `quota` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '配额，0表示使用默认值',
  `usage` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '使用量',
  `max_size` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '单个配置大小上限，单位为字节，0表示使用默认值',
  `max_aggr_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '聚合子配置最大个数',
  `max_aggr_size` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '单个聚合数据的子配置大小上限，单位为字节，0表示使用默认值',
  `max_history_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '最大变更历史数量',
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_tenant_id` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='租户容量信息表';
 
 
CREATE TABLE `tenant_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `kp` varchar(128) NOT NULL COMMENT 'kp',
  `tenant_id` varchar(128) default '' COMMENT 'tenant_id',
  `tenant_name` varchar(128) default '' COMMENT 'tenant_name',
  `tenant_desc` varchar(256) DEFAULT NULL COMMENT 'tenant_desc',
  `create_source` varchar(32) DEFAULT NULL COMMENT 'create_source',
  `gmt_create` bigint(20) NOT NULL COMMENT '创建时间',
  `gmt_modified` bigint(20) NOT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_tenant_info_kptenantid` (`kp`,`tenant_id`),
  KEY `idx_tenant_id` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='tenant_info';
 
CREATE TABLE users (
    username varchar(50) NOT NULL PRIMARY KEY,
    password varchar(500) NOT NULL,
    enabled boolean NOT NULL
);
 
CREATE TABLE roles (
    username varchar(50) NOT NULL,
    role varchar(50) NOT NULL,
    constraint uk_username_role UNIQUE (username,role)
);
 
CREATE TABLE permissions (
    role varchar(50) NOT NULL,
    resource varchar(512) NOT NULL,
    action varchar(8) NOT NULL,
    constraint uk_role_permission UNIQUE (role,resource,action)
);
 
INSERT INTO users (username, password, enabled) VALUES ('nacos', '$2a$10$EuWPZHzz32dJN7jexM34MOeYirDdFAZm2kuWj7VEOJhhZkDrxfvUu', TRUE);
 
INSERT INTO roles (username, role) VALUES ('nacos', 'ROLE_ADMIN');
```
docker pull nacos/nacos-server
```
docker run -d \
-e MODE=standalone \
-e PREFER_HOST_MODE=hostname \
-e SPRING_DATASOURCE_PLATFORM=mysql \
-e MYSQL_SERVICE_HOST=192.168.225.128 \
-e MYSQL_SERVICE_PORT=3306 \
-e MYSQL_SERVICE_USER=root \
-e MYSQL_SERVICE_PASSWORD=root \
-e MYSQL_SERVICE_DB_NAME=nacos \
-p 8848:8848 \
--name nacos \
--restart=always \
nacos/nacos-server
```
接着挂载目录：

mkdir -p /mount/docker/nacos/{logs,init.d,data}    

        
vim /mount/docker/nacos/init.d/custom.properties        #修改配置文件

```cnf
server.contextPath=/nacos
server.servlet.contextPath=/nacos
server.port=8848

spring.datasource.platform=mysql
db.num=1
#修改IP地址
db.url.0=jdbc:mysql://192.168.225.128:3306/nacos_config? characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true #这里需要修改端口
db.user=root #用户名
db.password=root #密码

nacos.cmdb.dumpTaskInterval=3600
nacos.cmdb.eventTaskInterval=10
nacos.cmdb.labelTaskInterval=300
nacos.cmdb.loadDataAtStart=false
management.metrics.export.elastic.enabled=false
management.metrics.export.influx.enabled=false
server.tomcat.accesslog.enabled=true
server.tomcat.accesslog.pattern=%h %l %u %t "%r" %s %b %D %{User-Agent}i
nacos.security.ignore.urls=/,/**/*.css,/**/*.js,/**/*.html,/**/*.map,/**/*.svg,/**/*.png,/**/*.ico,/console-fe/public/**,/v1/auth/login,/v1/console/health/**,/v1/cs/**,/v1/ns/**,/v1/cmdb/**,/actuator/**,/v1/console/server/**
nacos.naming.distro.taskDispatchThreadCount=1
nacos.naming.distro.taskDispatchPeriod=200
nacos.naming.distro.batchSyncKeyCount=1000
nacos.naming.distro.initDataRatio=0.9
nacos.naming.distro.syncRetryDelay=5000
nacos.naming.data.warmup=true
nacos.naming.expireInstance=true
```
docker  run \
--name nacos -itd \
-p 8848:8848 \
--privileged=true \
--restart=always \
-e JVM_XMS=256m \
-e JVM_XMX=256m \
-e MODE=standalone \
-e PREFER_HOST_MODE=hostname \
-v /mount/docker/nacos/conf:/home/nacos/conf \
-v /mount/docker/nacos/logs:/home/nacos/logs \
-v /mount/docker/nacos/data:/home/nacos/data \
nacos/nacos-server


## minio/minio
```
docker pull minio/minio

mkdir -p /mount/docker/minio/{config,data}


```
docker run -p 9000:9000 -p 9090:9090 \
     --name minio \
     -d --restart=always \
     -e "MINIO_ACCESS_KEY=minioadmin" \
     -e "MINIO_SECRET_KEY=minioadmin" \
     -v /mount/docker/minio/data:/data \
     -v /mount/docker/minio/config:/root/.minio \
     minio/minio server \
     /data --console-address ":9090" -address ":9000"

```     

 注意： docker最新版安装会报错 ，提示port问题，因为最新版提供了api和console两个端口，所以需要--console-address ":9000" --address ":9090" 进行指定启动，前期版本不需要，直接运行即可

## .安装docker-compose

最新发行的版本地址：https://github.com/docker/compose/releases
运行以下命令以下载Docker Compose的当前稳定版本：
 curl -SL https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose


将可执行权限应用于二进制文件：
sudo chmod +x /usr/local/bin/docker-compose

docker compose version

**直接移除二进制包即可**

sudo rm /usr/local/bin/docker-compose
### docker-compose使用
Compose是用于定义和运行多容器Docker应用程序的工具。
概念:

Compose 中有两个比较重要的概念： 服务service 和 项目 project。
服务 service :就是一个应用容器，实际上可以包含多个使用相同镜像运行的容器实例。
项目就是包含了多个 service 的一个 docker-compose.yml 文件
安装




子命令补齐
先安装 BASH 自身的子命令补全软件包

yum install bash-completion
1
curl -L https://raw.githubusercontent.com/docker/compose/1.27.4/contrib/completion/bash/docker-compose -o /etc/bash_completion.d/docker-compose
1
退出并重新登录即可
[root@docker ~]# docker-compose #连按两下tab键
build    create   events   help     kill     pause    ps       push     rm       scale    stop     unpause  version  
config   down     exec     images   logs     port     pull     restart  run      start    top      up 
1
2
3
docker-compose基础命令
首先在一个指定的目录中编辑一个 docker-compose.yml 文件
version: "3.8"                     # 指定要使用 docker-compose 的版本
services:                          # 声明服务
  host1:                           # 第一个服务的名称，可以设置多个服务
    image: "centos:7"              # 从这个镜像启动一个容器
    container_name: "host1"        # 容器启动后的名称
    stdin_open: true               # 相当于 docker run 的 -i    
    tty: true                      # 相当于 docker run 的 -t
    #command: /bin/bash            # 一开始执行的命令 
    networks:                      # 设置这个服务的网络信息
      centos_net:                  # 网络名称，需要在下面顶级的 networks 中声明
        ipv4_address: 172.16.1.10  # 指定一个静态的 IP 地址

networks:                          # 顶级 networks ，设置整个 docker-compose 使用的网络设备
  centos_net:                      # 网络设备名称
    driver: bridge                 # 网络设备是网桥，可以理解为是一个交换机设备
    ipam:                          # 顶层网络部分中相应的网络配置必须具有ipam块
      driver: default              # 采用的默认的网络模式
      config:                      # 下面是一个配置列表
        - subnet: 172.16.1.0/24    # 子网网络
          gateway: 172.16.1.1      # 网关


以后台的方式运行: up -d
注意：默认情况下，所有的 docker-compose 命令都必须在含有 docker-compose.yml 文件的目录下执行。换句话说，执行 docker-compose 命令的时候，需要保证当前目录下有 docker-compose.yml 文件。

docker-compose up -d
1
[root@docker compose]# docker-compose up -d
Creating network "compose_centos_net" with driver "bridge"
Creating host1 ... done
[root@docker compose]# 
1
2
3
4
列出当前 docker-compose 管理的所有的容器: ps
docker-compose ps
1
[root@docker compose]# docker-compose ps
Name     Command    State   Ports
---------------------------------
host1   /bin/bash   Up           
[root@docker compose]# 
1
2
3
4
5
列出当前 docker-compose 管理的所有的服务: ps --services
 docker-compose ps --services 
1
[root@docker compose]# docker-compose ps --services
host1
1
2
执行容器内的命令：exec
docker-compose exec 服务名 命令 [选项]
1
[root@docker compose]#  docker-compose exec host1 hostname -i
172.16.1.10
1
2
执行容器内的 bash 命令，就会进入容器
[root@docker compose]# docker-compose exec host1 bash
[root@c41b52ba3aab /]# hostname -i
172.16.1.10
[root@c41b52ba3aab /]# 
1
2
3
4
执行容器内的 exit 命令，就会退出容器
[root@c41b52ba3aab /]# exit
exit
[root@docker compose]# 
1
2
3
停止/启动容器: stop
在不移除容器的情况下停止运行容器。
之后，可以使用“docker compose start”重新启动它们。

stop [options] [--] [SERVICE...]
1
[root@docker compose]# docker-compose stop 
Stopping host1 ... done
[root@docker compose]# 
[root@docker compose]# docker-compose start
Starting host1 ... done
[root@docker compose]# docker-compose restart
Restarting host1 ... done
[root@docker compose]# docker ps
CONTAINER ID   IMAGE      COMMAND       CREATED             STATUS         PORTS     NAMES
c41b52ba3aab   centos:7   "/bin/bash"   About an hour ago   Up 5 seconds             host1
[root@docker compose]# docker-compose ps
Name     Command    State   Ports
---------------------------------

15
移除/删除/销毁容器：down
down 子命令，用于处于 Up 状态的容器停止，并删除容器、网络、卷和映像。

默认情况下删除如下内容：

compose 文件中为服务定义的容器
compose 文件中顶级的 networks 定义的网络设备
默认网络，如果使用了
放心，它不会删除 external 使用的外部网络和卷。

选项 -v 可以一同删除 compose 文件中定义的卷，默认是不删除的。

[root@docker compose]# docker-compose down 
Stopping host1 ... done
Removing host1 ... done
Removing network compose_centos_net
[root@docker compose]# 
```
## xxl-job-admin
mkdir -p /mount/docker/xxl-job/admin/logs



docker create --name xxl-job-admin -p 8088:8080 \
-e PARAMS="\
--spring.datasource.url=jdbc:mysql://172.17.0.3:3306/xxl_job?Unicode=true&characterEncoding=UTF-8 \
--spring.datasource.username=root \
--spring.datasource.password=root" \
-v /mount/docker/xxl-job/admin/logs:/data/applogs \
--privileged=true \
xuxueli/xxl-job-admin:2.3.1

## mongoDB
**拉取mongo镜像**

>docker pull mongo:4.4

创建mongo数据持久化目录
>mkdir -p /docker_volume/mongodb/data

运行容器
>docker run -itd --name mongo  -p 27017:27017 mongo --auth

-v: 将宿主机的/docker_volume/mongodb/data映射到容器的/data/db目录，将数据持久化到宿主机，以防止删除容器后，容器内的数据丢失–auth：需要密码才能访问容器服务
**创建用户**
登录mongo容器，并进入到【admin】数据库
> docker exec -it mongo mongosh
use admin

创建一个用户，mongo 默认没有用户
>db.createUser({ user:'root',pwd:'123456',roles:[ { role:'userAdminAnyDatabase', db: 'admin'},'readWriteAnyDatabase']});

【user:‘root’ 】：设置用户名为root
【pwd:‘123456’】：设置密码为123456
【role:‘userAdminAnyDatabase’】：只在admin数据库中可用，赋予用户所有数据库的userAdmin权限
【db: ‘admin’】：可操作的数据库
【‘readWriteAnyDatabase’】：赋予用户读写权限

dbAdmin：允许用户在指定数据库中执行管理函数，如索引创建、删除，查看统计或访问system.profile



# docker compose
sudo curl -L https://get.daocloud.io/docker/compose/releases/download/1.25.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

mkdir -p ./compose/reggie/nginx/{logs,html,conf.d,conf}

```yml
version: '0.1'
services:
  nginx:
#     build:
#       context: ./nginx
    restart: always
    container_name: nginx
    volumes:
    - ./nginx/conf.d:/etc/nginx/conf.d 
    - ./nginx/logs:/var/log/nginx 
    - ./nginx/html:/usr/share/nginx/html 
    - ./nginx/conf/nginx.conf:/etc/nginx/nginx.conf
    image: nginx@1.23.3
    ports:
      - 63342:63342
    networks:
      net:
networks:
    net:
volumes:
    vol:
```    

