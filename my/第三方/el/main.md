# 安装

## 部署单点es

### 创建网络

因为我们还需要部署kibana容器，因此需要让es和kibana容器互联。这里先创建一个网络：

```sh
docker network create es-net
```



### 加载镜像

这里我们采用elasticsearch的8.11.1版本的镜像，运行docker命令，部署单点es：

```shell
docker run -d \
	--name es \
    -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
    -e "discovery.type=single-node" \
    -v es-data:/usr/share/elasticsearch/data \
    -v es-plugins:/usr/share/elasticsearch/plugins \
    --privileged \
    --network es-net \
    -p 9200:9200 \
    -p 9300:9300 \
elasticsearch::8.11.1
```

命令解释：

- `-e "cluster.name=es-docker-cluster"`：设置集群名称
- `-e "http.host=0.0.0.0"`：监听的地址，可以外网访问
- `-e "ES_JAVA_OPTS=-Xms512m -Xmx512m"`：内存大小
- `-e "discovery.type=single-node"`：非集群模式
- `-v es-data:/usr/share/elasticsearch/data`：挂载逻辑卷，绑定es的数据目录
- `-v es-logs:/usr/share/elasticsearch/logs`：挂载逻辑卷，绑定es的日志目录
- `-v es-plugins:/usr/share/elasticsearch/plugins`：挂载逻辑卷，绑定es的插件目录
- `--privileged`：授予逻辑卷访问权
- `--network es-net` ：加入一个名为es-net的网络中
- `-p 9200:9200`：端口映射配置



在浏览器中输入：`http://192.168.150.101:9200 `即可看到elasticsearch的响应结果：

![Alt text](image.png)





## 部署kibana

kibana可以给我们提供一个elasticsearch的可视化界面，便于我们学习。

### 部署

运行docker命令，部署kibana

```sh
docker run -d \
--name kibana \
-e ELASTICSEARCH_HOSTS=http://es:9200 \
--network=es-net \
-p 5601:5601  \
kibana:7.12.1
```

- `--network es-net` ：加入一个名为es-net的网络中，与elasticsearch在同一个网络中
- `-e ELASTICSEARCH_HOSTS=http://es:9200"`：设置elasticsearch的地址，因为kibana已经与elasticsearch在一个网络，因此可以用容器名直接访问elasticsearch
- `-p 5601:5601`：端口映射配置

kibana启动一般比较慢，需要多等待一会，可以通过命令：

```sh
docker logs -f kibana
```

此时，在浏览器输入地址访问：http://192.168.150.101:5601，即可看到结果
![Alt text](image-1.png)
## DevTools

kibana中提供了一个DevTools界面：

![Alt text](image-2.png)

这个界面中可以编写DSL来操作elasticsearch。并且对DSL语句有自动补全功能。



## 安装IK分词器



### 在线安装ik插件

```shell
# 进入容器内部
docker exec -it elasticsearch /bin/bash

# 在线下载并安装
./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v8.11.0/elasticsearch-analysis-ik-8.11.0.zip

#退出
exit
#重启容器
docker restart elasticsearch
```

### 安装ik插件
插件下载地址
`https://github.com/medcl/elasticsearch-analysis-ik/releases`
#### 查看数据卷目录

安装插件需要知道elasticsearch的plugins目录位置，而我们用了数据卷挂载，因此需要查看elasticsearch的数据卷目录，通过下面命令查看:

```sh
docker volume inspect es-plugins
```

显示结果：

```json
[
    {
        "CreatedAt": "2022-05-06T10:06:34+08:00",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/es-plugins/_data",
        "Name": "es-plugins",
        "Options": null,
        "Scope": "local"
    }
]
```

说明plugins目录被挂载到了：`/var/lib/docker/volumes/es-plugins/_data `这个目录中。



#### 解压缩分词器安装包

下载的ik分词器解压缩，重命名为ik

#### 上传到es容器的插件数据卷中

也就是`/var/lib/docker/volumes/es-plugins/_data `：


#### 重启容器

```shell
# 4、重启容器
docker restart es
```

```sh
# 查看es日志
docker logs -f es
```

#### 测试：

IK分词器包含两种模式：

* `ik_smart`：最少切分

* `ik_max_word`：最细切分



```json
GET /_analyze
{
  "analyzer": "ik_smart",
  "text": "java狼人爱坤"
}
```

结果：

```json
{
  "tokens": [
    {
      "token": "java",
      "start_offset": 0,
      "end_offset": 4,
      "type": "ENGLISH",
      "position": 0
    },
    {
      "token": "狼人",
      "start_offset": 4,
      "end_offset": 6,
      "type": "CN_WORD",
      "position": 1
    },
    {
      "token": "爱",
      "start_offset": 6,
      "end_offset": 7,
      "type": "CN_CHAR",
      "position": 2
    },
    {
      "token": "坤",
      "start_offset": 7,
      "end_offset": 8,
      "type": "CN_CHAR",
      "position": 3
    }
  ]
}
```





### 扩展词词典

随着互联网的发展，“造词运动”也越发的频繁。出现了很多新的词语，在原有的词汇列表中并不存在，比如我们的爱坤就被分开，不被当作一组词汇。

所以我们的词汇也需要不断的更新，IK分词器提供了扩展词汇的功能。

1）打开IK分词器config目录

2）在IKAnalyzer.cfg.xml配置文件内容添加：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
        <comment>IK Analyzer 扩展配置</comment>
        <!--用户可以在这里配置自己的扩展字典 *** 添加扩展词典-->
        <entry key="ext_dict">ext.dic</entry>
</properties>
```

3）新建一个 ext.dic，可以参考config目录下复制一个配置文件进行修改

```properties
奥力给
```

4）重启elasticsearch 

```sh
docker restart es

# 查看 日志
docker logs -f elasticsearch
```

日志中已经成功加载ext.dic配置文件

5）测试效果：

```json
GET /_analyze
{
  "analyzer": "ik_max_word",
  "text": "奥力给！"
}
```

> 注意当前文件的编码必须是 UTF-8 格式，严禁使用Windows记事本编辑

### 停用词词典

在互联网项目中，在网络间传输的速度很快，所以很多语言是不允许在网络上传递的，如：关于宗教、政治等敏感词语，那么我们在搜索时也应该忽略当前词汇。

IK分词器也提供了强大的停用词功能，让我们在索引时就直接忽略当前的停用词汇表中的内容。

1）IKAnalyzer.cfg.xml配置文件内容添加：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
        <comment>IK Analyzer 扩展配置</comment>
        <!--用户可以在这里配置自己的扩展字典-->
        <entry key="ext_dict">ext.dic</entry>
         <!--用户可以在这里配置自己的扩展停止词字典  *** 添加停用词词典-->
        <entry key="ext_stopwords">stopword.dic</entry>
</properties>
```

3）在 stopword.dic 添加停用词

```properties
奥利奥
```

4）重启elasticsearch 

```sh
# 重启服务
docker restart elasticsearch
docker restart kibana

# 查看 日志
docker logs -f elasticsearch
```

日志中已经成功加载stopword.dic配置文件

5）测试效果：

```json
GET /_analyze
{
  "analyzer": "ik_max_word",
  "text": "奥利奥都点赞,奥力给！"
}
```

> 注意当前文件的编码必须是 UTF-8 格式，严禁使用Windows记事本编辑

## docker-compose安装
我们需要安装docker-compose，在一个文件夹下创建docker-compose.yml,然后在文件夹创建./es/plugins目录
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
      
    # volumes:
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



# 初识elasticsearch

## 了解ES


### elasticsearch的作用

elasticsearch是一款非常强大的开源搜索引擎，具备非常多强大功能，可以帮助我们从海量数据中快速找到需要的内容

例如：

- **在GitHub搜索代码**

  ![Alt text](image-3.png)

- **在电商网站搜索商品**
![Alt text](image-4.png)
  



### **ELK技术栈**

elasticsearch结合kibana、Logstash、Beats，也就是elastic stack（ELK）。被广泛应用在日志数据分析、实时监控等领域：

![Alt text](image-6.png)



而elasticsearch是elastic stack的核心，负责存储、搜索、分析数据。

![Alt text](image-7.png)


### elasticsearch和lucene

elasticsearch底层是基于**lucene**来实现的。

**Lucene**是一个Java语言的搜索引擎类库，是Apache公司的顶级项目，由DougCutting于1999年研发。官网地址：https://lucene.apache.org/ 。

![Alt text](image-8.png)




**elasticsearch**的发展历史：

- 2004年Shay Banon基于Lucene开发了Compass
- 2010年Shay Banon 重写了Compass，取名为Elasticsearch。

![Alt text](image-9.png)



## 倒排索引

倒排索引的概念是基于MySQL这样的正向索引而言的.所以在介绍倒排索引之前,我们先回顾正向索引

### 正向索引

那么什么是正向索引呢？例如给下表（tb_goods）中的id创建索引：

![Alt text](image-10.png)
如果是根据id查询，那么直接走索引，查询速度非常快。



但如果是基于title做模糊查询，只能是逐行扫描数据，流程如下：

1. 用户搜索数据，条件是title符合`"%手机%"`

2. 逐行获取数据，比如id为1的数据

3. 判断数据中的title是否符合用户搜索条件

4. 如果符合则放入结果集，不符合则丢弃。回到步骤1

因此在进行模糊查询大量数据时,便会效率低下,造成性能瓶颈,所以为了解决模糊查询效率低的问题,倒排索引便应运而生.

### 倒排索引

倒排索引中有两个非常重要的概念：

- **文档（`Document`）**：用来搜索的数据，其中的每一条数据就是一个文档。例如一个网页、一个商品信息
- **词条（`Term`）**：对文档数据或用户搜索数据，利用某种算法分词，得到的具备含义的词语就是词条。例如：我是中国人，就可以分为：我、是、中国人、中国、国人这样的几个词条

**创建倒排索引**是对正向索引的一种特殊处理，流程如下：

- 将每一个文档的数据利用算法分词，得到一个个词条
- 创建表，每行数据包括词条、词条所在文档id、位置等信息
- 因为词条唯一性，可以给词条创建索引，例如hash表结构索引

如图：

![Alt text](image-11.png)





倒排索引的**搜索流程**如下（以搜索"华为手机"为例）：

1）用户输入条件`"华为手机"`进行搜索。

2）对用户输入内容**分词**，得到词条：`华为`、`手机`。

3）拿着词条在倒排索引中查找，可以得到包含词条的文档id：1、2、3。

4）拿着文档id到正向索引中查找具体文档。

如图：

![Alt text](image-12.png)


虽然要先查询倒排索引，再查询倒排索引，但是无论是词条、还是文档id都建立了索引，查询速度非常快！无需全表扫描。



### 正向和倒排

那么为什么一个叫做正向索引，一个叫做倒排索引呢？

- **正向索引**是最传统的，根据id索引的方式。但根据词条查询时，必须先逐条获取每个文档，然后判断文档中是否包含所需要的词条，是**根据文档找词条的过程**。

- 而**倒排索引**则相反，是先找到用户要搜索的词条，根据词条得到保护词条的文档的id，然后根据id获取文档。是**根据词条找文档的过程**。


**对比优缺点**:

**正向索引**：

- 优点：
  - 可以给多个字段创建索引
  - 根据索引字段搜索、排序速度非常快
- 缺点：
  - 根据非索引字段，或者索引字段中的部分词条查找时，只能全表扫描。

**倒排索引**：

- 优点：
  - 根据词条搜索、模糊搜索时，速度非常快
- 缺点：
  - 只能给词条创建索引，而不是字段
  - 无法根据字段做排序





## es概念

elasticsearch中有很多独有的概念，与mysql中略有差别，但也有相似之处。

### 文档和字段

elasticsearch是面向**文档（Document）**存储的，可以是数据库中的一条商品数据，一个订单信息。文档数据会被序列化为json格式后存储在elasticsearch中：

![Alt text](image-13.png)

而Json文档中往往包含很多的**字段（Field）**，类似于数据库中的列。

###  索引和映射

**索引（Index）**，就是相同类型的文档的集合。

例如：

- 所有用户文档，就可以组织在一起，称为用户的索引；
- 所有商品的文档，可以组织在一起，称为商品的索引；
- 所有订单的文档，可以组织在一起，称为订单的索引；

![Alt text](image-14.png)


因此，我们可以把索引当做是数据库中的表。

数据库的表会有约束信息，用来定义表的结构、字段的名称、类型等信息。因此，索引库中就有**映射（mapping）**，是索引中文档的字段约束信息，类似表的结构约束。



### mysql与elasticsearch

我们统一的把**mysql**与**elasticsearch**的概念做一下对比：

| **MySQL** | **Elasticsearch** | **说明**      |
| --------- | ----------------- | --------------------- |
| Table     | Index             | 索引(index)，就是文档的集合，类似数据库的表(table)           |
| Row       | Document          | 文档（Document），就是一条条的数据，类似数据库中的行（Row），文档都是JSON格式 |
| Column    | Field             | 字段（Field），就是JSON文档中的字段，类似数据库中的列（Column） |
| Schema    | Mapping           | Mapping（映射）是索引中文档的约束，例如字段类型约束。类似数据库的表结构（Schema） |
| SQL       | DSL               | DSL是elasticsearch提供的JSON风格的请求语句，用来操作elasticsearch，实现CRUD |

是不是说，我们学习了elasticsearch就不再需要mysql了呢？

并不是如此，两者各自有自己的擅长支出：

- Mysql：擅长事务类型操作，可以确保数据的安全和一致性

- Elasticsearch：擅长海量数据的搜索、分析、计算



因此在企业中，往往是两者结合使用：

- 对安全性要求较高的写操作，使用mysql实现
- 对查询性能要求较高的搜索需求，使用elasticsearch实现
- 两者再基于某种方式，实现数据的同步，保证一致性



## 安装es、kibana,分词器
### 安装
可以参考这篇文章
`https://blog.csdn.net/studycodeday/article/details/134451772`
 


# 索引库操作

索引库就类似数据库表，mapping映射就类似表的结构。

我们要向es中存储数据，必须先创建“库”和“表”。



## mapping映射属性

mapping是对索引库中文档的约束，常见的mapping属性包括：

- type：字段数据类型，常见的简单类型有：
  - 字符串：text（可分词的文本）、keyword（精确值，例如：品牌、国家、ip地址）
  - 数值：long、integer、short、byte、double、float、
  - 布尔：boolean
  - 日期：date
  - 对象：object
- index：是否创建索引，默认为true
- analyzer：使用哪种分词器
- properties：该字段的子字段

**格式**:
```json
{
    "age": 21,
    "weight": 52.1,
    "isMarried": false,
    "info": "程序员Java讲师",
    "email": "zy@qq.cn",
    "score": [99.1, 99.5, 98.9],
    "name": {
        "firstName": "云",
        "lastName": "赵"
    }
}
```

对应的每个字段映射（mapping）：

- **age**：类型为 integer；参与搜索，因此需要index为true；无需分词器
- **weight**：类型为float；参与搜索，因此需要index为true；无需分词器
- **isMarried**：类型为boolean；参与搜索，因此需要index为true；无需分词器
- **info**：类型为字符串，需要分词，因此是text；参与搜索，因此需要index为true；分词器可以用ik_smart
- **email**：类型为字符串，但是不需要分词，因此是keyword；不参与搜索，因此需要index为false；无需分词器
- **score**：虽然是数组，但是我们只看元素的类型，类型为float；参与搜索，因此需要index为true；无需分词器
- **name**：类型为object，需要定义多个子属性
  - **name.firstName**；类型为字符串，但是不需要分词，因此是keyword；参与搜索，因此需要index为true；无需分词器
  - **name.lastName**；类型为字符串，但是不需要分词，因此是keyword；参与搜索，因此需要index为true；无需分词器


## 索引库的CRUD（创建，读取，更新，删除）

### 创建索引库和映射

#### 基本语法：

- 请求方式：PUT
- 请求路径：/索引库名，可以自定义
- 请求参数：mapping映射

**格式**：

```json
PUT /索引库名称
{
  "mappings": {
    "properties": {
      "字段名":{
        "type": "text",
        "analyzer": "ik_smart"
      },
      "字段名2":{
        "type": "keyword",
        "index": "false"
      },
      "字段名3":{
        "properties": {
          "子字段": {
            "type": "keyword"
          }
        }
      }
      // ...略
    }
  }
}
```



#### 示例：

```sh
PUT /onenewcode
{
  "mappings":{
    "properties":{
      "info":{
        "type":"text",
        "analyzer":"ik_smart"
      },
      "email":{
        "type":"keyword",
        "index":false
      },
      "name":{
        "properties":{
          "firstName":{
            "type":"keyword"
          }
        }
      }
      // ... 略
    }
  }
}
```
![Alt text](image-16.png)
### 查询索引库

**基本语法**：

- 请求方式：GET

- 请求路径：/索引库名

- 请求参数：无

**格式**：

```
GET /索引库名
```
![Alt text](image-17.png)


**示例**：

![Alt text](image-5.png)


### 修改索引库

倒排索引结构虽然不复杂，但是一旦数据结构改变（比如改变了分词器），就需要重新创建倒排索引，这简直是灾难。因此索引库**一旦创建，无法修改mapping**。



虽然无法修改mapping中已有的字段，但是却允许添加新的字段到mapping中，因为不会对倒排索引产生影响。

**语法说明**：

```json
PUT /索引库名/_mapping
{
  "properties": {
    "新字段名":{
      "type": "integer"
    }
  }
}
```



### 删除索引库

**语法：**

- 请求方式：DELETE

- 请求路径：/索引库名

- 请求参数：无

**格式：**

```
DELETE /索引库名
```
![Alt text](image-15.png)
# 文档操作

## 新增文档

**语法：**

```json
POST /索引库名/_doc/文档id
{
    "字段1": "值1",
    "字段2": "值2",
    "字段3": {
        "子属性1": "值3",
        "子属性2": "值4"
    },
    // ...
}
```

**示例：**

```json
POST /onenewcode/_doc/1
{
    "info": "程序员Java讲师",
    "email": "zy@qq.cn",
    "name": {
        "firstName": "云",
        "lastName": "赵"
    }
}
```

**响应：**

![Alt text](image-18.png)



## 查询文档

根据rest风格，新增是post，查询应该是get，不过查询一般都需要条件，这里我们把文档id带上。

**语法：**

```json
GET /{索引库名称}/_doc/{id}
```

**通过kibana查看数据：**

```js
GET /onenewcode/_doc/1
```

**查看结果：**

![Alt text](image-19.png)



## 删除文档

删除使用DELETE请求，同样，需要根据id进行删除：

**语法：**

```js
DELETE /{索引库名}/_doc/id值
```

**示例：**

```json
# 根据id删除数据
DELETE /onenewcode/_doc/1
```

**结果：**

![Alt text](image-20.png)



## 修改文档

修改有两种方式：

- 全量修改：直接覆盖原来的文档
- 增量修改：修改文档中的部分字段



### 全量修改

全量修改是覆盖原来的文档，其本质是：

- 根据指定的id删除文档
- 新增一个相同id的文档

**注意**：如果根据id删除时，id不存在，第二步的新增也会执行，也就从修改变成了新增操作了。



**语法：**

```json
PUT /{索引库名}/_doc/文档id
{
    "字段1": "值1",
    "字段2": "值2",
    // ... 略
}

```



**示例：**

```json
PUT /onenewcode/_doc/1
{
    "info": "程序员高级Java讲师",
    "email": "zy@qq.cn",
    "name": {
        "firstName": "云",
        "lastName": "赵"
    }
}
```



### 增量修改

增量修改是只修改指定id匹配的文档中的部分字段。

**语法：**

```json
POST /{索引库名}/_update/文档id
{
    "doc": {
         "字段名": "新的值",
    }
}
```



**示例：**

```json
POST /onenewcode/_update/1
{
  "doc": {
    "email": "ZhaoYun@qq.cn"
  }
}
```



# RestAPI

ES官方提供了各种不同语言的客户端，用来操作ES。这些客户端的本质就是组装DSL语句，通过http请求发送给ES。官方文档地址：https://www.elastic.co/guide/en/elasticsearch/client/index.html

之前官方提供了Java Rest Client又包括两种：

- Java Low Level Rest Client
- Java High Level Rest Client

但是在最新版中官方已经推出新版的客户端：
Elasticsearch Java API Client 
接下来本文的所有教程也是基于此库

## Demo工程

### 导入数据

数据库数据：



数据结构如下：

```sql
CREATE TABLE `tb_hotel` (
  `id` bigint(20) NOT NULL COMMENT '酒店id',
  `name` varchar(255) NOT NULL COMMENT '酒店名称；例：7天酒店',
  `address` varchar(255) NOT NULL COMMENT '酒店地址；例：航头路',
  `price` int(10) NOT NULL COMMENT '酒店价格；例：329',
  `score` int(2) NOT NULL COMMENT '酒店评分；例：45，就是4.5分',
  `brand` varchar(32) NOT NULL COMMENT '酒店品牌；例：如家',
  `city` varchar(32) NOT NULL COMMENT '所在城市；例：上海',
  `star_name` varchar(16) DEFAULT NULL COMMENT '酒店星级，从低到高分别是：1星到5星，1钻到5钻',
  `business` varchar(255) DEFAULT NULL COMMENT '商圈；例：虹桥',
  `latitude` varchar(32) NOT NULL COMMENT '纬度；例：31.2497',
  `longitude` varchar(32) NOT NULL COMMENT '经度；例：120.3925',
  `pic` varchar(255) DEFAULT NULL COMMENT '酒店图片；例:/img/1.jpg',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 导入项目



### mapping映射分析

创建索引库，最关键的是mapping映射，而mapping映射要考虑的信息包括：

- 字段名
- 字段数据类型
- 是否参与搜索
- 是否需要分词
- 如果分词，分词器是什么？

其中：

- 字段名、字段数据类型，可以参考数据表结构的名称和类型
- 是否参与搜索要分析业务来判断，例如图片地址，就无需参与搜索
- 是否分词呢要看内容，内容如果是一个整体就无需分词，反之则要分词
- 分词器，我们可以统一使用ik_max_word



来看下酒店数据的索引库结构:

```json
PUT /hotel
{
  "mappings": {
    "properties": {
      "id": {
        "type": "keyword"
      },
      "name":{
        "type": "text",
        "analyzer": "ik_max_word",
        "copy_to": "all"
      },
      "address":{
        "type": "keyword",
        "index": false
      },
      "price":{
        "type": "integer"
      },
      "score":{
        "type": "integer"
      },
      "brand":{
        "type": "keyword",
        "copy_to": "all"
      },
      "city":{
        "type": "keyword",
        "copy_to": "all"
      },
      "starName":{
        "type": "keyword"
      },
      "business":{
        "type": "keyword"
      },
      "location":{
        "type": "geo_point"
      },
      "pic":{
        "type": "keyword",
        "index": false
      },
      "all":{
        "type": "text",
        "analyzer": "ik_max_word"
      }
    }
  }
}
```



几个特殊字段说明：

- location：地理坐标，里面包含精度、纬度
- all：一个组合字段，其目的是将多字段的值 利用copy_to合并，提供给用户搜索



地理坐标说明：

![Alt text](image-21.png)

copy_to说明：

![Alt text](image-22.png)



### 初始化RestClient

在elasticsearch提供的API中，与elasticsearch一切交互都封装在一个名为ElasticsearchClient的类中，必须先完成这个对象的初始化，建立与elasticsearch的连接。



1）引入es的RestHighLevelClient依赖：

```groovy
plugins {
    id 'org.springframework.boot' version '3.0.2'
    id 'io.spring.dependency-management' version '1.1.0'
    id 'java'
}

group = 'com.example'
version = '0.0.1-SNAPSHOT'
sourceCompatibility = '17'

repositories {
    mavenCentral()
}
// 强制实行是统一格式编码
tasks.withType(JavaCompile) {
    options.encoding = "utf-8"
}
tasks.withType(Javadoc) {
    options.encoding = "utf-8"
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter'
//    implementation 'org.springframework.boot:spring-boot-starter-data-elasticsearch'
    implementation('co.elastic.clients:elasticsearch-java:8.5.3')
//    implementation 'com.fasterxml.jackson.core:jackson-databind:2.12.3'
    implementation  'com.baomidou:mybatis-plus-boot-starter:3.5.3.2'
    compileOnly 'org.projectlombok:lombok:1.18.30'
    annotationProcessor 'org.projectlombok:lombok:1.18.30'
    implementation('mysql:mysql-connector-java:8.0.33')
    implementation('com.alibaba:fastjson:2.0.32')
    implementation('org.apache.commons:commons-lang3')
    implementation 'org.springframework.boot:spring-boot-starter-web'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}

tasks.named('test') {
    useJUnitPlatform()
}


```




2）初始化es客户端：

初始化的代码如下：

```java
@Configuration
public class ESConfig {
    @Value("${spring.elasticsearch.uris}")
    private String urls;

    @Bean
    public ElasticsearchClient ESConfigClient(){
        System.out.println(urls);
         // Create the low-level client 创建低级客户端
         RestClient restClient = RestClient
                 .builder(HttpHost.create(urls)).build();
         // 创建json映射器
        ElasticsearchTransport transport=new RestClientTransport(restClient,new JacksonJsonpMapper());
        // 创建api客户端
        return new ElasticsearchClient(transport);
     }
}


```



这里为了单元测试方便，我们创建一个测试类HotelIndexTest，然后将初始化的类注入测试类中：

```java
package com.onenewcode.esdemo;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch.core.GetResponse;
import co.elastic.clients.elasticsearch.core.IndexResponse;
import com.alibaba.fastjson.JSON;
import com.onenewcode.esdemo.pojo.Hotel;
import com.onenewcode.esdemo.pojo.HotelDoc;
import com.onenewcode.esdemo.service.impl.HotelService;
import org.elasticsearch.client.RequestOptions;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.io.IOException;
import java.util.List;

/**
 * @author 29071
 * @version 1.0
 * @data 2023/11/20 8:57
 */
@SpringBootTest
 class HotelDocumentTest {
    @Autowired
    private ElasticsearchClient esClient;
    @Autowired
    HotelService hotelService;

}

```





## 创建索引库

### 代码解读


代码分为三步：

- 1）创建CreateIndexRequest 对象。因为是创建索引库的操作.
- 2）添加请求参数，其实就是DSL的JSON参数部分。因为json字符串很长，这里是定义了静态字符串常量MAPPING_TEMPLATE，让代码看起来更加优雅。
```java
CreateIndexRequest  request = CreateIndexRequest.of(i -> i
                .index("hotel")
                .withJson(new StringReader(MAPPING_TEMPLATE))
        );
        //构建是否存在的请求
boolean response =esClient.indices().create(request).acknowledged();
```



### 完整示例
在项目的constants包下，创建一个类，定义mapping映射的JSON字符串常量：

```java


public class HotelConstants {
    public static final String MAPPING_TEMPLATE = "{\n" +
            "  \"mappings\": {\n" +
            "    \"properties\": {\n" +
            "      \"id\": {\n" +
            "        \"type\": \"keyword\"\n" +
            "      },\n" +
            "      \"name\":{\n" +
            "        \"type\": \"text\",\n" +
            "        \"analyzer\": \"ik_max_word\",\n" +
            "        \"copy_to\": \"all\"\n" +
            "      },\n" +
            "      \"address\":{\n" +
            "        \"type\": \"keyword\",\n" +
            "        \"index\": false\n" +
            "      },\n" +
            "      \"price\":{\n" +
            "        \"type\": \"integer\"\n" +
            "      },\n" +
            "      \"score\":{\n" +
            "        \"type\": \"integer\"\n" +
            "      },\n" +
            "      \"brand\":{\n" +
            "        \"type\": \"keyword\",\n" +
            "        \"copy_to\": \"all\"\n" +
            "      },\n" +
            "      \"city\":{\n" +
            "        \"type\": \"keyword\",\n" +
            "        \"copy_to\": \"all\"\n" +
            "      },\n" +
            "      \"starName\":{\n" +
            "        \"type\": \"keyword\"\n" +
            "      },\n" +
            "      \"business\":{\n" +
            "        \"type\": \"keyword\"\n" +
            "      },\n" +
            "      \"location\":{\n" +
            "        \"type\": \"geo_point\"\n" +
            "      },\n" +
            "      \"pic\":{\n" +
            "        \"type\": \"keyword\",\n" +
            "        \"index\": false\n" +
            "      },\n" +
            "      \"all\":{\n" +
            "        \"type\": \"text\",\n" +
            "        \"analyzer\": \"ik_max_word\"\n" +
            "      }\n" +
            "    }\n" +
            "  }\n" +
            "}";
}
```



的HotelIndexTest测试类中，编写单元测试，实现创建索引：

```java
   @Test
    void testCreateIndex() throws IOException {
//     设置索引库名称，并读取json设置映射关系
        CreateIndexRequest  request = CreateIndexRequest.of(i -> i
                .index("hotel")
                .withJson(new StringReader(MAPPING_TEMPLATE))
        );
        //构建是否存在的请求
        ExistsRequest existsRequest = ExistsRequest.of(i->i.index("hotel"));

        if (esClient.indices().exists(existsRequest).value()){
            System.out.println("该索引已经存在");
        }else {
//            创建新索引
            boolean response =esClient.indices().create(request).acknowledged();
        }
    }
```



## 删除索引库

删除索引库的DSL语句非常简单：

```json
DELETE /hotel
```

与创建索引库相比：

- 请求方式从PUT变为DELTE
- 请求路径不变
- 无请求参数

所以代码的差异，注意体现在Request对象上。依然是三步走：


在hotel-demo中的HotelIndexTest测试类中，编写单元测试，实现删除索引：

```java
@Test
    void testDeleteIndex() throws IOException {
        esClient.indices().delete(c -> c
                .index("hotel")
        );
    }
```







# RestClient操作文档

为了与索引库操作分离，我们再次参加一个测试类，做两件事情：

- 初始化ElasticsearchClient
- 我们的酒店数据在数据库，需要利用IHotelService去查询，所以注入这个接口

```java


@SpringBootTest
public class HotelDocumentTest {
    @Autowired
    private ElasticsearchClient esClient;
    @Autowired
    HotelService hotelService;


}

```





## 新增文档

我们要将数据库的酒店数据查询出来，写入elasticsearch中。

### 索引库实体类

数据库查询后的结果是一个Hotel类型的对象。结构如下：

```java
@Data
@TableName("tb_hotel")
public class Hotel {
    @TableId(type = IdType.INPUT)
    private Long id;
    private String name;
    private String address;
    private Integer price;
    private Integer score;
    private String brand;
    private String city;
    private String starName;
    private String business;
    private String longitude;
    private String latitude;
    private String pic;
}
```

与我们的索引库结构存在差异：

- longitude和latitude需要合并为location

因此，我们需要定义一个新的类型，与索引库结构吻合：

```java


@Data
@NoArgsConstructor
public class HotelDoc {
    private Long id;
    private String name;
    private String address;
    private Integer price;
    private Integer score;
    private String brand;
    private String city;
    private String starName;
    private String business;
    private String location;
    private String pic;

    public HotelDoc(Hotel hotel) {
        this.id = hotel.getId();
        this.name = hotel.getName();
        this.address = hotel.getAddress();
        this.price = hotel.getPrice();
        this.score = hotel.getScore();
        this.brand = hotel.getBrand();
        this.city = hotel.getCity();
        this.starName = hotel.getStarName();
        this.business = hotel.getBusiness();
        this.location = hotel.getLatitude() + ", " + hotel.getLongitude();
        this.pic = hotel.getPic();
    }
}

```



### 语法说明

新增文档的DSL语句如下：

```json
POST /{索引库名}/_doc/1
{
    "name": "Jack",
    "age": 21
}
```


### 完整代码

我们导入酒店数据，基本流程一致，但是需要考虑几点变化：

- 酒店数据来自于数据库，我们需要先查询出来，得到hotel对象
- hotel对象需要转为HotelDoc对象
- HotelDoc需要序列化为json格式


在HotelDocumentTest测试类中，编写单元测试：

```java
   @Test
    void testAddDocument() throws IOException {
        // 1.查询数据库hotel数据
        Hotel hotel = hotelService.getById(61083L);
        // 2.转换为HotelDoc
        HotelDoc hotelDoc = new HotelDoc(hotel);
        IndexResponse response = esClient.index(i -> i
                .index("hotel")
                .id(hotelDoc.getId().toString())
                .document(hotelDoc)
        );
    }
```





## 查询文档

### 语法说明

查询的DSL语句如下：

```json
GET /hotel/_doc/{id}
```

非常简单，因此代码大概分两步：

- 准备Request对象
- 发送请求

不过查询的目的是得到结果，解析为HotelDoc，因此难点是结果的解析。完整代码如下：



### 完整代码

在HotelDocumentTest测试类中，编写单元测试：

```java
    @Test
    void testGetDocumentById() throws IOException {
        GetResponse<HotelDoc> response = esClient.get(g -> g
                        .index("hotel") //选择索引库
                        .id("61083"),
                HotelDoc.class //选择查询对象的映射
        );

        if (response.found()) {
            //获取结果
            HotelDoc hotelDoc = response.source();
            System.out.println("查询结果"+hotelDoc);
        } else {
            System.out.println("未查询到数据");
        }
    }
```





## 删除文档

删除的DSL为是这样的：

```json
DELETE /hotel/_doc/{id}
```

与查询相比，仅仅是请求方式从DELETE变成GET.

在hotel-demo的HotelDocumentTest测试类中，编写单元测试：
```java
@Test
    void testDeleteDocumentById() throws IOException {
        esClient.delete(d -> d.index("hotel").id("61083"));
    }

```







## 批量导入文档

案例需求：利用BulkRequest批量将数据库数据导入到索引库中。

步骤如下：

- 利用mybatis-plus查询酒店数据

- 将查询到的酒店数据（Hotel）转换为文档类型数据（HotelDoc）

- 利用JavaRestClient中的BulkRequest批处理，实现批量新增文档



### 完整代码

在HotelDocumentTest测试类中，编写单元测试：

```java
    @Test
    void testBulkRequest() throws IOException {
        // 查询所有的酒店数据
        List<Hotel> list = hotelService.list();
        // 循环遍历
        list.forEach(i->//循环闭包
        {
            try {//捕捉异常
                esClient.index(
                        x-> x.index("hotel").id(i.getId().toString())
                                .document(new HotelDoc(i)));
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        });
    }
```




# DSL查询文档

elasticsearch的查询依然是基于JSON风格的DSL来实现的。

## DSL查询分类

Elasticsearch提供了基于JSON的DSL（[Domain Specific Language](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)）来定义查询。常见的查询类型包括：

- **查询所有**：查询出所有数据，一般测试用。例如：match_all

- **全文检索（full text）查询**：利用分词器对用户输入内容分词，然后去倒排索引库中匹配。例如：
  - match_query
  - multi_match_query
- **精确查询**：根据精确词条值查找数据，一般是查找keyword、数值、日期、boolean等类型字段。例如：
  - ids
  - range
  - term
- **地理（geo）查询**：根据经纬度查询。例如：
  - geo_distance
  - geo_bounding_box
- **复合（compound）查询**：复合查询可以将上述各种查询条件组合起来，合并查询条件。例如：
  - bool
  - function_score



查询的语法基本一致：

```json
GET /indexName/_search
{
  "query": {
    "查询类型": {
      "查询条件": "条件值"
    }
  }
}
```

我们以查询所有为例，其中：

- 查询类型为match_all
- 没有查询条件

```json
// 查询所有
GET /indexName/_search
{
  "query": {
    "match_all": {
    }
  }
}
```

其它查询无非就是**查询类型**、**查询条件**的变化。



## 全文检索查询



### 使用场景

全文检索查询的基本流程如下：

- 对用户搜索的内容做分词，得到词条
- 根据词条去倒排索引库中匹配，得到文档id
- 根据文档id找到文档，返回给用户

比较常用的场景包括：

- 商城的输入框搜索
- 百度输入框搜索

### 基本语法

常见的全文检索查询包括：

- match查询：单字段查询
- multi_match查询：多字段查询，任意一个字段符合条件就算符合查询条件

match查询语法如下：

```json
GET /indexName/_search
{
  "query": {
    "match": {
      "FIELD": "TEXT"
    }
  }
}
```

mulit_match语法如下：

```json
GET /indexName/_search
{
  "query": {
    "multi_match": {
      "query": "TEXT",
      "fields": ["FIELD1", " FIELD12"]
    }
  }
}
```



### 示例

match查询示例：

![Alt text](image-23.png)



multi_match查询示例：
![Alt text](image-24.png)



可以看到，两种查询结果是一样的，为什么？

因为我们将brand、name、business值都利用copy_to复制到了all字段中。因此你根据三个字段搜索，和根据all字段搜索效果当然一样了。

但是，搜索字段越多，对查询性能影响越大，因此建议采用copy_to，然后单字段查询的方式。



## 精准查询

精确查询一般是查找keyword、数值、日期、boolean等类型字段。所以**不会**对搜索条件分词。常见的有：

- term：根据词条精确值查询
- range：根据值的范围查询

### term查询

因为精确查询的字段搜是不分词的字段，因此查询的条件也必须是**不分词**的词条。查询时，用户输入的内容跟自动值完全匹配时才认为符合条件。如果用户输入的内容过多，反而搜索不到数据。



语法说明：

```json
// term查询
GET /indexName/_search
{
  "query": {
    "term": {
      "FIELD": {
        "value": "VALUE"
      }
    }
  }
}
```



示例：

当我搜索的是精确词条时，能正确查询出结果：

![Alt text](image-25.png)
但是，当我搜索的内容不是词条，而是多个词语形成的短语时，反而搜索不到：

![Alt text](image-26.png)




### range查询

范围查询，一般应用在对数值类型做范围过滤的时候。比如做价格范围过滤。



基本语法：

```json
// range查询
GET /indexName/_search
{
  "query": {
    "range": {
      "FIELD": {
        "gte": 10, // 这里的gte代表大于等于，gt则代表大于
        "lte": 20 // lte代表小于等于，lt则代表小于
      }
    }
  }
}
```



示例：

![Alt text](image-27.png)


### 总结

精确查询常见的有哪些？

- term查询：根据词条精确匹配，一般搜索keyword类型、数值类型、布尔类型、日期类型字段
- range查询：根据数值范围查询，可以是数值、日期的范围

## 地理坐标查询

所谓的地理坐标查询，其实就是根据经纬度查询，官方文档：https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-queries.html

常见的使用场景包括：

- 携程：搜索我附近的酒店
- 滴滴：搜索我附近的出租车
- 微信：搜索我附近的人



附近的酒店：
![Alt text](image-28.png)

附近的车：

![Alt text](image-29.png)


###  矩形范围查询

矩形范围查询，也就是geo_bounding_box查询，查询坐标落在某个矩形范围的所有文档：
![Alt text](image-30.png)

查询时，需要指定矩形的**左上**、**右下**两个点的坐标，然后画出一个矩形，落在该矩形内的都是符合条件的点。

语法如下：

```json
// geo_bounding_box查询
GET /indexName/_search
{
  "query": {
    "geo_bounding_box": {
      "FIELD": {
        "top_left": { // 左上点
          "lat": 31.1,
          "lon": 121.5
        },
        "bottom_right": { // 右下点
          "lat": 30.9,
          "lon": 121.7
        }
      }
    }
  }
}
```
### 附近查询

附近查询，也叫做距离查询（geo_distance）：查询到指定中心点小于某个距离值的所有文档。
换句话来说，在地图上找一个点作为圆心，以指定距离为半径，画一个圆，落在圆内的坐标都算符合条件：


语法说明：

```json
// geo_distance 查询
GET /indexName/_search
{
  "query": {
    "geo_distance": {
      "distance": "15km", // 半径
      "FIELD": "31.21,121.5" // 圆心
    }
  }
}
```
示例：

我们先搜索陆家嘴附近15km的酒店：

![Alt text](image-31.png)
发现共有47家酒店。



然后把半径缩短到3公里：
![Alt text](image-32.png)

可以发现，搜索到的酒店数量减少到了5家。

## 复合查询

复合（compound）查询：复合查询可以将其它简单查询组合起来，实现更复杂的搜索逻辑。常见的有两种：

- fuction score：算分函数查询，可以控制文档相关性算分，控制文档排名
- bool query：布尔查询，利用逻辑关系组合多个其它的查询，实现复杂搜索

### 相关性算分

当我们利用match查询时，文档结果会根据与搜索词条的关联度打分（_score），返回结果时按照分值降序排列。

例如，我们搜索 "虹桥如家"，结果如下：

```json
[
  {
    "_score" : 17.850193,
    "_source" : {
      "name" : "虹桥如家酒店真不错",
    }
  },
  {
    "_score" : 12.259849,
    "_source" : {
      "name" : "外滩如家酒店真不错",
    }
  },
  {
    "_score" : 11.91091,
    "_source" : {
      "name" : "迪士尼如家酒店真不错",
    }
  }
]
```



elasticsearch新版采用的算法为BM25算法，公式如下：
![Alt text](image-33.png)







### 算分函数查询

根据相关度打分是比较合理的需求，但**合理的不一定是产品经理需要**的。

以百度为例，你搜索的结果中，并不是相关度越高排名越靠前，而是谁掏的钱多排名就越靠前。如图：
![Alt text](image-34.png)


要想认为控制相关性算分，就需要利用elasticsearch中的function score 查询了。



#### 1）语法说明

![Alt text](image-35.png)


function score 查询中包含四部分内容：

- **原始查询**条件：query部分，基于这个条件搜索文档，并且基于BM25算法给文档打分，**原始算分**（query score）
- **过滤条件**：filter部分，符合该条件的文档才会重新算分
- **算分函数**：符合filter条件的文档要根据这个函数做运算，得到的**函数算分**（function score），有四种函数
  - weight：函数结果是常量
  - field_value_factor：以文档中的某个字段值作为函数结果
  - random_score：以随机数作为函数结果
  - script_score：自定义算分函数算法
- **运算模式**：算分函数的结果、原始查询的相关性算分，两者之间的运算方式，包括：
  - multiply：相乘
  - replace：用function score替换query score
  - 其它，例如：sum、avg、max、min



function score的运行流程如下：

- 1）根据**原始条件**查询搜索文档，并且计算相关性算分，称为**原始算分**（query score）
- 2）根据**过滤条件**，过滤文档
- 3）符合**过滤条件**的文档，基于**算分函数**运算，得到**函数算分**（function score）
- 4）将**原始算分**（query score）和**函数算分**（function score）基于**运算模式**做运算，得到最终结果，作为相关性算分。



因此，其中的关键点是：

- 过滤条件：决定哪些文档的算分被修改
- 算分函数：决定函数算分的算法
- 运算模式：决定最终算分结果



#### 2）示例

需求：给“如家”这个品牌的酒店排名靠前一些

翻译一下这个需求，转换为之前说的四个要点：

- 原始条件：不确定，可以任意变化
- 过滤条件：brand = "如家"
- 算分函数：可以简单粗暴，直接给固定的算分结果，weight
- 运算模式：比如求和

因此最终的DSL语句如下：

```json
GET /hotel/_search
{
  "query": {
    "function_score": {
      "query": {  .... }, // 原始查询，可以是任意条件
      "functions": [ // 算分函数
        {
          "filter": { // 满足的条件，品牌必须是如家
            "term": {
              "brand": "如家"
            }
          },
          "weight": 2 // 算分权重为2
        }
      ],
      "boost_mode": "sum" // 加权模式，求和
    }
  }
}
```







#### 3）小结

function score query定义的三要素是什么？

- 过滤条件：哪些文档要加分
- 算分函数：如何计算function score
- 加权方式：function score 与 query score如何运算



### 布尔查询

布尔查询是一个或多个查询子句的组合，每一个子句就是一个**子查询**。子查询的组合方式有：

- must：必须匹配每个子查询，类似“与”
- should：选择性匹配子查询，类似“或”
- must_not：必须不匹配，**不参与算分**，类似“非”
- filter：必须匹配，**不参与算分**



比如在搜索酒店时，除了关键字搜索外，我们还可能根据品牌、价格、城市等字段做过滤：

![Alt text](image-36.png)
每一个不同的字段，其查询的条件、方式都不一样，必须是多个不同的查询，而要组合这些查询，就必须用bool查询了。



需要注意的是，搜索时，参与**打分的字段越多，查询的性能也越差**。因此这种多条件查询时，建议这样做：

- 搜索框的关键字搜索，是全文检索查询，使用must查询，参与算分
- 其它过滤条件，采用filter查询。不参与算分



#### 1）语法示例：

```json
GET /hotel/_search
{
  "query": {
    "bool": {
      "must": [
        {"term": {"city": "上海" }}
      ],
      "should": [
        {"term": {"brand": "皇冠假日" }},
        {"term": {"brand": "华美达" }}
      ],
      "must_not": [
        { "range": { "price": { "lte": 500 } }}
      ],
      "filter": [
        { "range": {"score": { "gte": 45 } }}
      ]
    }
  }
}
```



#### 2）示例

需求：搜索名字包含“如家”，价格不高于400，在坐标31.21,121.5周围10km范围内的酒店。

分析：

- 名称搜索，属于全文检索查询，应该参与算分。放到must中
- 价格不高于400，用range查询，属于过滤条件，不参与算分。放到must_not中
- 周围10km范围内，用geo_distance查询，属于过滤条件，不参与算分。放到filter中


![Alt text](image-37.png)




#### 3）小结

bool查询有几种逻辑关系？

- must：必须匹配的条件，可以理解为“与”
- should：选择性匹配的条件，可以理解为“或”
- must_not：必须不匹配的条件，不参与打分
- filter：必须匹配的条件，不参与打分



# 搜索结果处理

搜索的结果可以按照用户指定的方式去处理或展示。

## 排序

elasticsearch默认是根据相关度算分（_score）来排序，但是也支持自定义方式对搜索[结果排序](https://www.elastic.co/guide/en/elasticsearch/reference/current/sort-search-results.html)。可以排序字段类型有：keyword类型、数值类型、地理坐标类型、日期类型等。

### 普通字段排序

keyword、数值、日期类型排序的语法基本一致。

**语法**：

```json
GET /indexName/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "FIELD": "desc"  // 排序字段、排序方式ASC、DESC
    }
  ]
}
```

排序条件是一个数组，也就是可以写多个排序条件。按照声明的顺序，当第一个条件相等时，再按照第二个条件排序，以此类推



**示例**：

需求描述：酒店数据按照用户评价（score)降序排序，评价相同的按照价格(price)升序排序

![Alt text](image-38.png)


### 地理坐标排序

地理坐标排序略有不同。

**语法说明**：

```json
GET /indexName/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "_geo_distance" : {
          "FIELD" : "纬度，经度", // 文档中geo_point类型的字段名、目标坐标点
          "order" : "asc", // 排序方式
          "unit" : "km" // 排序的距离单位
      }
    }
  ]
}
```

这个查询的含义是：

- 指定一个坐标，作为目标点
- 计算每一个文档中，指定字段（必须是geo_point类型）的坐标 到目标点的距离是多少
- 根据距离排序



**示例：**

需求描述：实现对酒店数据按照到你的位置坐标的距离升序排序

提示：获取你的位置的经纬度的方式：https://lbs.amap.com/demo/jsapi-v2/example/map/click-to-get-lnglat/



假设我的位置是：31.034661，121.612282，寻找我周围距离最近的酒店。

![Alt text](image-39.png)



## 分页

elasticsearch 默认情况下只返回top10的数据。而如果要查询更多数据就需要修改分页参数了。elasticsearch中通过修改from、size参数来控制要返回的分页结果：

- from：从第几个文档开始
- size：总共查询几个文档

类似于mysql中的`limit ?, ?`

### 基本的分页

分页的基本语法如下：

```json
GET /hotel/_search
{
  "query": {
    "match_all": {}
  },
  "from": 0, // 分页开始的位置，默认为0
  "size": 10, // 期望获取的文档总数
  "sort": [
    {"price": "asc"}
  ]
}
```





### 深度分页问题

现在，我要查询990~1000的数据，查询逻辑要这么写：

```json
GET /hotel/_search
{
  "query": {
    "match_all": {}
  },
  "from": 990, // 分页开始的位置，默认为0
  "size": 10, // 期望获取的文档总数
  "sort": [
    {"price": "asc"}
  ]
}
```

这里是查询990开始的数据，也就是 第990~第1000条 数据。

不过，elasticsearch内部分页时，必须先查询 0~1000条，然后截取其中的990 ~ 1000的这10条：

![Alt text](image-40.png)


查询TOP1000，如果es是单点模式，这并无太大影响。

但是elasticsearch将来一定是集群，例如我集群有5个节点，我要查询TOP1000的数据，并不是每个节点查询200条就可以了。

因为节点A的TOP200，在另一个节点可能排到10000名以外了。

因此要想获取整个集群的TOP1000，必须先查询出每个节点的TOP1000，汇总结果后，重新排名，重新截取TOP1000。

![Alt text](image-41.png)

那如果我要查询9900~10000的数据呢？是不是要先查询TOP10000呢？那每个节点都要查询10000条？汇总到内存中？



当查询分页深度较大时，汇总数据过多，对内存和CPU会产生非常大的压力，因此elasticsearch会禁止from+ size 超过10000的请求。



针对深度分页，ES提供了两种解决方案，[官方文档](https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html)：

- search after：分页时需要排序，原理是从上一次的排序值开始，查询下一页数据。官方推荐使用的方式。
- scroll：原理将排序后的文档id形成快照，保存在内存。官方已经不推荐使用。



### 小结

分页查询的常见实现方案以及优缺点：

- `from + size`：
  - 优点：支持随机翻页
  - 缺点：深度分页问题，默认查询上限（from + size）是10000
  - 场景：百度、京东、谷歌、淘宝这样的随机翻页搜索
- `after search`：
  - 优点：没有查询上限（单次查询的size不超过10000）
  - 缺点：只能向后逐页查询，不支持随机翻页
  - 场景：没有随机翻页需求的搜索，例如手机向下滚动翻页

- `scroll`：
  - 优点：没有查询上限（单次查询的size不超过10000）
  - 缺点：会有额外内存消耗，并且搜索结果是非实时的
  - 场景：海量数据的获取和迁移。从ES7.1开始不推荐，建议用 after search方案。

## 高亮

### 高亮原理

什么是高亮显示呢？

我们在百度，京东搜索时，关键字会变成红色，比较醒目，这叫高亮显示：

![Alt text](image-42.png)

高亮显示的实现分为两步：

- 1）给文档中的所有关键字都添加一个标签，例如`<em>`标签
- 2）页面给`<em>`标签编写CSS样式


### 实现高亮

**高亮的语法**：

```json
GET /hotel/_search
{
  "query": {
    "match": {
      "FIELD": "TEXT" // 查询条件，高亮一定要使用全文检索查询
    }
  },
  "highlight": {
    "fields": { // 指定要高亮的字段
      "FIELD": {
        "pre_tags": "<em>",  // 用来标记高亮字段的前置标签
        "post_tags": "</em>" // 用来标记高亮字段的后置标签
      }
    }
  }
}
```


**注意：**

- 高亮是对关键字高亮，因此**搜索条件必须带有关键字**，而不能是范围这样的查询。
- 默认情况下，**高亮的字段，必须与搜索指定的字段一致**，否则无法高亮
- 如果要对非搜索字段高亮，则需要添加一个属性：required_field_match=false



**示例**：

![Alt text](image-43.png)




# Elasticsearch Java API 查询文档


## 快速入门

我们以match_all查询为例

### 发起查询请求

![Alt text](image-44.png)

**代码解读**：
上面的代码使用了流式编程的思想，首先选择用search表示是选择查询模式，然后用index决定搜索的索引库，然后用query构建查询索引,然后选择查询模式matchAll。

es中的查询语句
```json
GET hotel/_search
{
  "query": {
    "match_all": {}
  }
}
```


### 解析响应


elasticsearch返回的结果是一个JSON字符串，结构包含：

- `hits`：命中的结果
  - `total`：总条数，其中的value是具体的总条数值
  - `max_score`：所有结果中得分最高的文档的相关性算分
  - `hits`：搜索结果的文档数组，其中的每个文档都是一个json对象
    - `source`：文档中的原始数据，也是json转化成实体类的对象

因此，我们解析响应结果，就是逐层解析JSON字符串，流程如下：

- `HitsMetadata`：通过response.hits()获取，就是JSON中的最外层的hits，代表命中的结果
  - `HitsMetadata.total().value()`：获取总条数信息
  - `SearchHits#getHits()`：获取SearchHit数组，也就是文档数组



### 完整代码

完整代码如下：

```java
    @Test
    void testMatchAll() throws IOException {
//进行查询
        SearchResponse<HotelDoc> response = esClient.search(s -> s
                        .index("hotel")
                        .query(q -> q
                                .matchAll(m->m)),
                HotelDoc.class
        );
        handleResponse(response);
    }
    private void handleResponse( SearchResponse<HotelDoc> response) {
        HitsMetadata<HotelDoc> searchHits = response.hits();
        // 4.1.总条数
        long total = searchHits.total().value();
        System.out.println("总条数：" + total);
        // 4.2.获取文档数组
        List<Hit<HotelDoc>>  hits = searchHits.hits();
        // 4.3.遍历
        hits.forEach(i->{
            // 4.4 自动序列化
            HotelDoc hotelDoc = i.source();
            // 4.6.处理高亮结果
            // 1）获取高亮字段和高亮数据的map
            Map<String, List<String>>  map = i.highlight();
            if (map!=null){
                // 2）根据字段名，获取高亮结果
                List<String> name = map.get("name");
                if (name!=null){
                    // 3）获取高亮结果字符串数组中的第1个元素
                    String hName= name.get(0);
                    // 4）把高亮结果放到HotelDoc中
                    hotelDoc.setName(hName);
                }
            }
            System.out.println(hotelDoc);
//            System.out.println(i.highlight());
        });

        }
```





## match查询

全文检索的match和multi_match查询与match_all的API基本一致。差别是查询条件，也就是query的部分。

![Alt text](image-45.png)


因此，Java代码上的差异主要是request.source().query()中的参数了。同样是利用QueryBuilders提供的方法：



而结果解析代码则完全一致，可以抽取并共享。



完整代码如下：

```java
    @Test
    void testMatch() throws IOException {

        SearchResponse<HotelDoc> response = esClient.search(i->i
                .index("hotel")
                .query(q->q.match(t->t
                        .field("all")//设置请求字段
                        .query("如家")//设置请求参数
                )),
                HotelDoc.class
        );
        handleResponse(response);
    }

```


## 精确查询

精确查询主要是两者：

- term：词条精确匹配
- range：范围查询

与之前的查询相比，差异同样在查询条件，其它都一样。

es语句
```json
GET /hotel/_search
{
  "query": {
    "match": {
      "all": "如家"
    }
  }
}
```

查询条件构造的API如下：
```java

        SearchResponse<HotelDoc> response = esClient.search(s -> s
                        .index("hotel")
                        .query(q->q.
                                    term(t->t
                                    .field("city")
                                    .value("上海"))),
```





## 布尔查询

布尔查询是用must、must_not、filter等方式组合其它查询，代码示例如下：



es语句
```json
GET /hotel/_search
{
  "query": {
    "match": {
      "all": "如家"
    }
  }
}
```




完整代码如下：

```java
    @Test
    void testMatch() throws IOException {

        SearchResponse<HotelDoc> response = esClient.search(i->i
                .index("hotel")
                .query(q->q.match(t->t
                        .field("all")//设置请求字段
                        .query("如家")//设置请求参数
                )),
                HotelDoc.class
        );
        handleResponse(response);
    }
```



## 排序、分页

es语句
```json
GET hotel/_search
{
  "query": {
    "match_all": {}
  },
  "from": 0,
  "size": 5,
  "sort": [
    {
      "price": {
        "order": "desc"
      }
    }
  ]

}
```



完整代码示例：

```java
@Test
void testPageAndSort() throws IOException {
    // 页码，每页大小
    int page = 1, size = 5;

    // 1.准备Request
    SearchRequest request = new SearchRequest("hotel");
    // 2.准备DSL
    // 2.1.query
    request.source().query(QueryBuilders.matchAllQuery());
    // 2.2.排序 sort
    request.source().sort("price", SortOrder.ASC);
    // 2.3.分页 from、size
    request.source().from((page - 1) * size).size(5);
    // 3.发送请求
    SearchResponse response = client.search(request, RequestOptions.DEFAULT);
    // 4.解析响应
    handleResponse(response);

}
```



## 高亮

高亮的代码与之前代码差异较大，有两点：

- 查询的DSL：其中除了查询条件，还需要添加高亮条件，同样是与query同级。
- 结果解析：结果除了要解析_source文档数据，还要解析高亮结果

### 高亮请求构建

es语句
```json
GET /hotel/_search
{
  "query": {
    "match": {
      "all": "如家"
    }
  },
  "highlight": {
    "fields": {"name": {"require_field_match": "false"}}
  }
}
```

上述代码省略了查询条件部分，但是大家不要忘了：高亮查询必须使用全文检索查询，并且要有搜索关键字，将来才可以对关键字高亮。

完整代码如下：

```java
    @Test
    void testHighlight() throws IOException {
        SearchResponse<HotelDoc> response = esClient.search(s->s
                        .index("hotel")
                        .query(q->q.match(t->t
                                .field("all")//设置请求字段
                                .query("如家")//设置请求参数
                        ))
                        .highlight(h->h
                                .fields("name",f->f.requireFieldMatch(false))),
                HotelDoc.class
        );
        handleResponse(response);
    }
```



### 高亮结果解析

高亮的结果与查询的文档结果默认是分离的，并不在一起。



代码解读：

- 第一步：从结果中获取source。hit.getSourceAsString()，这部分是非高亮结果，json字符串。还需要反序列为HotelDoc对象
- 第二步：获取高亮结果。hit.getHighlightFields()，返回值是一个Map，key是高亮字段名称，值是HighlightField对象，代表高亮值
- 第三步：从map中根据高亮字段名称，获取高亮字段值对象HighlightField
- 第四步：从HighlightField中获取Fragments，并且转为字符串。这部分就是真正的高亮字符串了
- 第五步：用高亮的结果替换HotelDoc中的非高亮结果



完整代码如下：

```java
private void handleResponse(SearchResponse response) {
    // 4.解析响应
    SearchHits searchHits = response.getHits();
    // 4.1.获取总条数
    long total = searchHits.getTotalHits().value;
    System.out.println("共搜索到" + total + "条数据");
    // 4.2.文档数组
    SearchHit[] hits = searchHits.getHits();
    // 4.3.遍历
    for (SearchHit hit : hits) {
        // 获取文档source
        String json = hit.getSourceAsString();
        // 反序列化
        HotelDoc hotelDoc = JSON.parseObject(json, HotelDoc.class);
        // 获取高亮结果
        Map<String, HighlightField> highlightFields = hit.getHighlightFields();
        if (!CollectionUtils.isEmpty(highlightFields)) {
            // 根据字段名获取高亮结果
            HighlightField highlightField = highlightFields.get("name");
            if (highlightField != null) {
                // 获取高亮值
                String name = highlightField.getFragments()[0].string();
                // 覆盖非高亮结果
                hotelDoc.setName(name);
            }
        }
        System.out.println("hotelDoc = " + hotelDoc);
    }
}
```





# 黑马旅游案例


我们实现四部分功能：

- 酒店搜索和分页
- 酒店结果过滤
- 我周边的酒店
- 酒店竞价排名



启动我们提供的es-demo项目，其默认端口是8089，访问http://localhost:8090，就能看到项目页面了：

![Alt text](image-46.png)




## 酒店搜索和分页

案例需求：实现黑马旅游的酒店搜索功能，完成关键字搜索和分页

### 需求分析

在项目的首页，有一个大大的搜索框，还有分页按钮：

![Alt text](image-47.png)

点击搜索按钮，可以看到浏览器控制台发出了请求：
![Alt text](image-48.png)

请求参数如下：

![Alt text](image-49.png)



由此可以知道，我们这个请求的信息如下：

- 请求方式：POST
- 请求路径：/hotel/list
- 请求参数：JSON对象，包含4个字段：
  - key：搜索关键字
  - page：页码
  - size：每页大小
  - sortBy：排序，目前暂不实现
- 返回值：分页查询，需要返回分页结果PageResult，包含两个属性：
  - `total`：总条数
  - `List<HotelDoc>`：当前页的数据



因此，我们实现业务的流程如下：

- 步骤一：定义实体类，接收请求参数的JSON对象
- 步骤二：编写controller，接收页面的请求
- 步骤三：编写业务实现，利用RestHighLevelClient实现搜索、分页



### 定义实体类

实体类有两个，一个是前端的请求参数实体，一个是服务端应该返回的响应结果实体。

1）请求参数

前端请求的json结构如下：

```json
{
    "key": "搜索关键字",
    "page": 1,
    "size": 3,
    "sortBy": "default"
}
```

因此，我们在`com.onenewcode.esdemo.pojo`包下定义一个实体类：

```java
package com.onenewcode.esdemo.pojo;

import lombok.Data;

@Data
public class RequestParams {
    private String key;
    private Integer page;
    private Integer size;
    private String sortBy;
}
```



2）返回值

分页查询，需要返回分页结果PageResult，包含两个属性：

- `total`：总条数
- `List<HotelDoc>`：当前页的数据

因此，我们在`com.onenewcode.esdemo.pojo`中定义返回结果：

```java
package com.onenewcode.esdemo.pojo;

import lombok.Data;

import java.util.List;

@Data
public class PageResult {
    private Long total;
    private List<HotelDoc> hotels;

    public PageResult() {
    }

    public PageResult(Long total, List<HotelDoc> hotels) {
        this.total = total;
        this.hotels = hotels;
    }
}
```



### 定义controller

定义一个HotelController，声明查询接口，满足下列要求：

- 请求方式：Post
- 请求路径：/hotel/list
- 请求参数：对象，类型为RequestParam
- 返回值：PageResult，包含两个属性
  - `Long total`：总条数
  - `List<HotelDoc> hotels`：酒店数据



因此，我们在`com.onenewcode.esdemo.web`中定义HotelController：

```java
@RestController
@RequestMapping("/hotel")
public class HotelController {

    @Autowired
    private IHotelService hotelService;
	// 搜索酒店数据
    @PostMapping("/list")
    public PageResult search(@RequestBody RequestParams params){
        return hotelService.search(params);
    }
}
```



### 实现搜索业务

我们在controller调用了IHotelService，并没有实现该方法，因此下面我们就在IHotelService中定义方法，并且去实现业务逻辑。

1）在`com.onenewcode.esdemo.service`中的`IHotelService`接口中定义一个方法：

```java
/**
 * 根据关键字搜索酒店信息
 * @param params 请求参数对象，包含用户输入的关键字 
 * @return 酒店文档列表
 */
PageResult search(RequestParams params);
```



2）实现搜索业务，肯定离不开ElasticsearchClient，我们需要把它注册到Spring中作为一个Bean。在`com.onenewcode.esdemo.config`中创建ESConfig：

```java
package com.onenewcode.esdemo.config;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.json.jackson.JacksonJsonpMapper;
import co.elastic.clients.transport.ElasticsearchTransport;
import co.elastic.clients.transport.rest_client.RestClientTransport;
import org.apache.http.HttpHost;
import org.elasticsearch.client.RestClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * @author 29071
 * @version 1.0
 * @data 2023/11/19 16:42
 */
@Configuration
public class ESConfig {
    @Value("${spring.elasticsearch.uris}")
    private String urls;

    @Bean
    public ElasticsearchClient ESConfigClient(){
        System.out.println(urls);
         // Create the low-level client 创建低级客户端
         RestClient restClient = RestClient
                 .builder(HttpHost.create(urls)).build();
         // 创建json映射器
        ElasticsearchTransport transport=new RestClientTransport(restClient,new JacksonJsonpMapper());
        // 创建api客户端
        return new ElasticsearchClient(transport);
     }
}

```

3）在`com.onenewcode.esdemo.service.impl`中的`HotelService`中实现search方法：

```java
    @Override
    public PageResult search(RequestParams params) throws IOException {
        String key=params.getKey();
        int page = params.getPage();
        int size = params.getSize();
        SearchResponse<HotelDoc> request=esClient.search(s->s
                .index("hotel")
                .query(q->q
                        .bool(b->b
                                .must(m->{
                    if (key==null||"".equals(key)){
                        return m.matchAll(ma->ma);
                    }else {
                        return m.match(ms->ms.field("all").query(key));
                    }
                })))
                        .size(size)
                        .from((page - 1) * size),
                HotelDoc.class);

        return handleResponse(request);
    }
  // 结果解析
    private PageResult handleResponse(SearchResponse<HotelDoc> response) {
        // 4.解析响应
        HitsMetadata<HotelDoc> searchHits = response.hits();
        // 4.1.获取总条数
        long total = searchHits.total().value();
        // 4.2.文档数组
        List<HotelDoc> hotels = searchHits.hits().stream().map(Hit::source).toList();
        // 4.4.封装返回
        return new PageResult(total, hotels);
    }
```
## 酒店结果过滤

需求：添加品牌、城市、星级、价格等过滤功能

### 需求分析

在页面搜索框下面，会有一些过滤项：

![Alt text](image-50.png)

传递的参数如图：

![Alt text](image-51.png) 

包含的过滤条件有：

- brand：品牌值
- city：城市
- minPrice~maxPrice：价格范围
- starName：星级

我们需要做两件事情：

- 修改请求参数的对象RequestParams，接收上述参数
- 修改业务逻辑，在搜索条件之外，添加一些过滤条件



### 修改实体类

修改在`com.onenewcode.esdemo.pojo`包下的实体类RequestParams：

```java
@Data
public class RequestParams {
    private String key;
    private Integer page;
    private Integer size;
    private String sortBy;
    // 下面是新增的过滤条件参数
    private String city;
    private String brand;
    private String starName;
    private Integer minPrice;
    private Integer maxPrice;
}
```



### 修改搜索业务

在HotelService的search方法中，只有一个地方需要修改：requet.source().query( ... )其中的查询条件。

在之前的业务中，只有match查询，根据关键字搜索，现在要添加条件过滤，包括：

- 品牌过滤：是keyword类型，用term查询
- 星级过滤：是keyword类型，用term查询
- 价格过滤：是数值类型，用range查询
- 城市过滤：是keyword类型，用term查询

多个查询条件组合，肯定是boolean查询来组合：

- 关键字搜索放到must中，参与算分
- 其它过滤条件放到filter中，不参与算分




代码如下：

```java
    @Override
    public PageResult search(RequestParams params) throws IOException {
        String key=params.getKey();
        int page = params.getPage();
        int size = params.getSize();
        List<Query> queryList=new ArrayList<>();
        if (params.getCity() != null && !params.getCity().equals(""))
            queryList.add(TermQuery.of(t->t.field("city").value(params.getCity()))._toQuery());

        if (params.getBrand() != null && !params.getBrand().equals(""))
            queryList.add(TermQuery.of(t->t.field("brand").value(params.getBrand()))._toQuery());

        if (params.getStarName() != null && !params.getStarName().equals(""))
            queryList.add(TermQuery.of(t -> t.field("starName").value(params.getStarName()))._toQuery());
        if (params.getMinPrice() != null && params.getMaxPrice() != null)
            queryList.add(RangeQuery.of(t->t.field("city").gte(JsonData.of(params.getMinPrice())).lte(JsonData.of(params.getMaxPrice())))._toQuery());


        SearchResponse<HotelDoc> request=esClient.search(s->s
                .index("hotel")
                .query(q->q
                        .bool(b->b
                                .must(m->{
                                    if (key==null||"".equals(key)){
                                        return m.matchAll(ma->ma);
                                    }else {
                                        return m.match(ms->ms.field("all").query(key));
                                            }
                                        })
                                .filter(queryList)
                            )
                        )
                .size(size)
                .from((page - 1) * size),
                HotelDoc.class);

        return handleResponse(request);
    }
```





## 我周边的酒店

需求：我附近的酒店

### 需求分析

在酒店列表页的右侧，有一个小地图，点击地图的定位按钮，地图会找到你所在的位置：

![Alt text](image-52.png)
并且，在前端会发起查询请求，将你的坐标发送到服务端：

![Alt text](image-53.png)


我们要做的事情就是基于这个location坐标，然后按照距离对周围酒店排序。实现思路如下：

- 修改RequestParams参数，接收location字段
- 修改search方法业务逻辑，如果location有值，添加根据geo_distance排序的功能



### 修改实体类

修改在`com.onenewcode.esdemo.pojo`包下的实体类RequestParams：

```java
package com.onenewcode.esdemo.pojo;

import lombok.Data;

@Data
public class RequestParams {
    private String key;
    private Integer page;
    private Integer size;
    private String sortBy;
    private String city;
    private String brand;
    private String starName;
    private Integer minPrice;
    private Integer maxPrice;
    // 我当前的地理坐标
    private String location;
}

```



### 距离排序API

我们以前学习过排序功能，包括两种：

- 普通字段排序
- 地理坐标排序

我们只讲了普通字段排序对应的java写法。地理坐标排序只学过DSL语法，如下：

```json
GET /indexName/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "price": "asc"  
    },
    {
      "_geo_distance" : {
          "FIELD" : "纬度，经度",
          "order" : "asc",
          "unit" : "km"
      }
    }
  ]
}
```




### 添加距离排序

在`com.onenewcode.esdemo.service.impl`的`HotelService`的`search`方法中，添加一个排序功能：


完整代码：

```java
@Override
public PageResult search(RequestParams params) {
    @Override
    public PageResult search(RequestParams params) throws IOException {
        String key=params.getKey();
        int page = params.getPage();
        int size = params.getSize();
        // 各种条件过滤
        List<Query> queryList=new ArrayList<>();
        if (params.getCity() != null && !params.getCity().equals(""))
            queryList.add(TermQuery.of(t->t.field("city").value(params.getCity()))._toQuery());

        if (params.getBrand() != null && !params.getBrand().equals(""))
            queryList.add(TermQuery.of(t->t.field("brand").value(params.getBrand()))._toQuery());

        if (params.getStarName() != null && !params.getStarName().equals(""))
            queryList.add(TermQuery.of(t -> t.field("starName").value(params.getStarName()))._toQuery());
        if (params.getMinPrice() != null && params.getMaxPrice() != null)
            queryList.add(RangeQuery.of(t->t.field("city").gte(JsonData.of(params.getMinPrice())).lte(JsonData.of(params.getMaxPrice())))._toQuery());
        // 设置金额排顺序，地理位置排序
        List<SortOptions> optionsList=new ArrayList<>();

        optionsList.add(SortOptions.of(s->s.field(f->f
                .field("price")
                .order(SortOrder.Asc))));
        if (params.getLocation() != null && !params.getLocation().equals(""))
            optionsList.add(SortOptions.of(s->s.geoDistance(g->g.field("location").location(l->l.text(params.getLocation())).unit(DistanceUnit.Kilometers))));

        SearchResponse<HotelDoc> request=esClient.search(s->s
                .index("hotel")
                .query(q->q
                        .bool(b->b
                                .must(m->{
                                    if (key==null||"".equals(key)){
                                        return m.matchAll(ma->ma);
                                    }else {
                                        return m.match(ms->ms.field("all").query(key));
                                            }
                                        })
                                .filter(queryList)
                            )
                        )
                .size(size)
                .from((page - 1) * size)
                .sort(optionsList)
                        ,
                HotelDoc.class);

        return handleResponse(request);
    }
```



### 排序距离显示

重启服务后，测试我的酒店功能：

![image-20210722100040674](assets/image-20210722100040674.png)



发现确实可以实现对我附近酒店的排序，不过并没有看到酒店到底距离我多远，这该怎么办？



排序完成后，页面还要获取我附近每个酒店的具体**距离**值，这个值在响应结果中是独立的：

![image-20210722095648542](assets/image-20210722095648542.png)

因此，我们在结果解析阶段，除了解析source部分以外，还要得到sort部分，也就是排序的距离，然后放到响应结果中。

我们要做两件事：

- 修改HotelDoc，添加排序距离字段，用于页面显示
- 修改HotelService类中的handleResponse方法，添加对sort值的获取



1）修改HotelDoc类，添加距离字段

```java
package com.onenewcode.esdemo.pojo;

import lombok.Data;
import lombok.NoArgsConstructor;


@Data
@NoArgsConstructor
public class HotelDoc {
    private Long id;
    private String name;
    private String address;
    private Integer price;
    private Integer score;
    private String brand;
    private String city;
    private String starName;
    private String business;
    private String location;
    private String pic;
    // 排序时的 距离值
    private Object distance;

    public HotelDoc(Hotel hotel) {
        this.id = hotel.getId();
        this.name = hotel.getName();
        this.address = hotel.getAddress();
        this.price = hotel.getPrice();
        this.score = hotel.getScore();
        this.brand = hotel.getBrand();
        this.city = hotel.getCity();
        this.starName = hotel.getStarName();
        this.business = hotel.getBusiness();
        this.location = hotel.getLatitude() + ", " + hotel.getLongitude();
        this.pic = hotel.getPic();
    }
}

```



2）修改HotelService中的handleResponse方法

![image-20210722100613966](assets/image-20210722100613966.png)



重启后测试，发现页面能成功显示距离了：

![image-20210722100838604](assets/image-20210722100838604.png)





## 4.4.酒店竞价排名

需求：让指定的酒店在搜索结果中排名置顶

### 4.4.1.需求分析

要让指定酒店在搜索结果中排名置顶，效果如图：

![image-20210722100947292](assets/image-20210722100947292.png)

页面会给指定的酒店添加**广告**标记。



那怎样才能让指定的酒店排名置顶呢？



我们之前学习过的function_score查询可以影响算分，算分高了，自然排名也就高了。而function_score包含3个要素：

- 过滤条件：哪些文档要加分
- 算分函数：如何计算function score
- 加权方式：function score 与 query score如何运算



这里的需求是：让**指定酒店**排名靠前。因此我们需要给这些酒店添加一个标记，这样在过滤条件中就可以**根据这个标记来判断，是否要提高算分**。

比如，我们给酒店添加一个字段：isAD，Boolean类型：

- true：是广告
- false：不是广告

这样function_score包含3个要素就很好确定了：

- 过滤条件：判断isAD 是否为true
- 算分函数：我们可以用最简单暴力的weight，固定加权值
- 加权方式：可以用默认的相乘，大大提高算分



因此，业务的实现步骤包括：

1. 给HotelDoc类添加isAD字段，Boolean类型

2. 挑选几个你喜欢的酒店，给它的文档数据添加isAD字段，值为true

3. 修改search方法，添加function score功能，给isAD值为true的酒店增加权重



### 4.4.2.修改HotelDoc实体

给`com.onenewcode.esdemo.pojo`包下的HotelDoc类添加isAD字段：

![image-20210722101908062](assets/image-20210722101908062.png)



### 4.4.3.添加广告标记

接下来，我们挑几个酒店，添加isAD字段，设置为true：

```json
POST /hotel/_update/1902197537
{
    "doc": {
        "isAD": true
    }
}
POST /hotel/_update/2056126831
{
    "doc": {
        "isAD": true
    }
}
POST /hotel/_update/1989806195
{
    "doc": {
        "isAD": true
    }
}
POST /hotel/_update/2056105938
{
    "doc": {
        "isAD": true
    }
}
```



### 4.4.4.添加算分函数查询

接下来我们就要修改查询条件了。之前是用的boolean 查询，现在要改成function_socre查询。



function_score查询结构如下：

![image-20210721191544750](assets/image-20210721191544750.png)



对应的JavaAPI如下：

![image-20210722102850818](assets/image-20210722102850818.png)



我们可以将之前写的boolean查询作为**原始查询**条件放到query中，接下来就是添加**过滤条件**、**算分函数**、**加权模式**了。所以原来的代码依然可以沿用。



修改`com.onenewcode.esdemo.service.impl`包下的`HotelService`类中的`buildBasicQuery`方法，添加算分函数查询：

```java
private void buildBasicQuery(RequestParams params, SearchRequest request) {
    // 1.构建BooleanQuery
    BoolQueryBuilder boolQuery = QueryBuilders.boolQuery();
    // 关键字搜索
    String key = params.getKey();
    if (key == null || "".equals(key)) {
        boolQuery.must(QueryBuilders.matchAllQuery());
    } else {
        boolQuery.must(QueryBuilders.matchQuery("all", key));
    }
    // 城市条件
    if (params.getCity() != null && !params.getCity().equals("")) {
        boolQuery.filter(QueryBuilders.termQuery("city", params.getCity()));
    }
    // 品牌条件
    if (params.getBrand() != null && !params.getBrand().equals("")) {
        boolQuery.filter(QueryBuilders.termQuery("brand", params.getBrand()));
    }
    // 星级条件
    if (params.getStarName() != null && !params.getStarName().equals("")) {
        boolQuery.filter(QueryBuilders.termQuery("starName", params.getStarName()));
    }
    // 价格
    if (params.getMinPrice() != null && params.getMaxPrice() != null) {
        boolQuery.filter(QueryBuilders
                         .rangeQuery("price")
                         .gte(params.getMinPrice())
                         .lte(params.getMaxPrice())
                        );
    }

    // 2.算分控制
    FunctionScoreQueryBuilder functionScoreQuery =
        QueryBuilders.functionScoreQuery(
        // 原始查询，相关性算分的查询
        boolQuery,
        // function score的数组
        new FunctionScoreQueryBuilder.FilterFunctionBuilder[]{
            // 其中的一个function score 元素
            new FunctionScoreQueryBuilder.FilterFunctionBuilder(
                // 过滤条件
                QueryBuilders.termQuery("isAD", true),
                // 算分函数
                ScoreFunctionBuilders.weightFactorFunction(10)
            )
        });
    request.source().query(functionScoreQuery);
}
```











