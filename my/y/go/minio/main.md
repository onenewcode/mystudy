# Minio概述

## 安装
我们采用docker方式安装，可以执行以下命令直接安装。
```go
docker run -p 9000:9000 -p 9090:9090 \
     --name minio \
     -d --restart=always \
     -e "MINIO_ACCESS_KEY=minioadmin" \
     -e "MINIO_SECRET_KEY=minioadmin" \
     minio/minio server \
     /data --console-address ":9090" -address ":9000"
```
# minio-go 介绍

## 快速开始
```go
package main

import (
	"github.com/minio/minio-go"
	"log"
)

var (
	MinioClient *minio.Client
)

const (
	endpoint        = "play.minio.io:9000"    //兼容对象存储服务endpoint,也可以设置自己的服务器地址
	accessKeyID     = "Q3AM3UQ867SPQQA43P2F"    // 对象存储的Access key
	secretAccessKey = "zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG"    /// 对象存储的Secret key
	ssl             = false //true代表使用HTTPS
)

func init() {
	// 初使化minio client对象。
	minioClient, err := minio.New("play.minio.io:9000", "Q3AM3UQ867SPQQA43P2F", "zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG", ssl)
	if err != nil {
		log.Println(err)
	} else {
		MinioClient = minioClient
	}
}
func main() {
	if MinioClient != nil {
		log.Println("链接服务器成功")
	}
}

```
如果在命令行显示`链接服务器成功`就代表我们的代码已经运行成功，我们之所以链接成功是因为现在是我们的是官方的服务器。之后我们可以改成我们自己的服务器。

