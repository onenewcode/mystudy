# springframework.beans.BeanUtils

复制类的属性到另一个类的属性需要同名、
```java
 BeanUtils.copyProperties(dto,courseMarket);
 ```
# apache.commons.lang.StringUtils
检测字符串 
```java
// 判断是否为null和长度是否为0
StringUtils.isNotEmpty(queryCourseParamsDto.getAuditStatus())
```
# javax.validation
检验数据类型
```java
 @NotEmpty(message = "添加课程名称不能为空",groups={ValidationGroups.Inster.class})
 @NotEmpty(message = "修改课程名称不能为空",groups={ValidationGroups.Update.class})
 @ApiModelProperty(value = "课程名称", required = true)
 private String name;kv
```
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```
<img src="./img/1.png">
# spring web
实现统一异常处理
```xml
Java
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-web</artifactId>
</dependency>
```
# log4j2
输出日志
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-log4j2</artifactId>
</dependency>
```

# OAuth2
过程
<img src="./img/2.png">

```java
public class AuthorizationServerConfigurerAdapter implements AuthorizationServerConfigurer {
    public AuthorizationServerConfigurerAdapter() {}
    public void configure(AuthorizationServerSecurityConfigurer security) throws Exception {}
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {}
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) throws Exception {}
}
```
1）ClientDetailsServiceConfigurer：用来配置客户端详情服务（ClientDetailsService），
随便一个客户端都可以随便接入到它的认证服务吗？答案是否定的，服务提供商会给批准接入的客户端一个身份，用于接入时的凭据，有客户端标识和客户端秘钥，在这里配置批准接入的客户端的详细信息。
2）AuthorizationServerEndpointsConfigurer：用来配置令牌（token）的访问端点和令牌服务(token services)。
3）AuthorizationServerSecurityConfigurer：用来配置令牌端点的安全约束.
2、TokenConfig为令牌策略配置类
暂时先使用InMemoryTokenStore在内存存储令牌，令牌的有效期等信息配置如下：
```java
    //令牌管理服务
    @Bean(name="authorizationServerTokenServicesCustom")
    public AuthorizationServerTokenServices tokenService() {
        DefaultTokenServices service=new DefaultTokenServices();
        service.setSupportRefreshToken(true);//支持刷新令牌
        service.setTokenStore(tokenStore);//令牌存储策略
        service.setAccessTokenValiditySeconds(7200); // 令牌默认有效期2小时
        service.setRefreshTokenValiditySeconds(259200); // 刷新令牌默认有效期3天
        return service;
    }
```

## 模式
### 密码模式

密码模式相对授权码模式简单，授权码模式需要借助浏览器供用户亲自授权

<img src="./img/3.png">

POST {{auth_host}}/auth/oauth/token?client_id=XcWebApp&client_secret=XcWebApp&grant_type=password&username=zhangsan&password=123

# JWT
JSON Web Token（JWT）是一种使用JSON格式传递数据的网络令牌技术，它是一个开放的行业标准（RFC 7519），它定义了一种简洁的、自包含的协议格式，用于在通信双方传递json对象，传递的信息经过数字签名可以被验证和信任，它可以使用HMAC算法或使用RSA的公钥/私钥对来签名，防止内容篡改。

## 特点
JWT令牌的优点：
1、jwt基于json，非常方便解析。
2、可以在令牌中自定义丰富的内容，易扩展。
3、通过非对称加密算法及数字签名技术，JWT防止篡改，安全性高。
4、资源服务使用JWT可不依赖认证服务即可完成授权。
缺点：
１、JWT令牌较长，占存储空间比较大。
## 内容
```s
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsicmVzMSJdLCJ1c2VyX25hbWUiOiJ6aGFuZ3NhbiIsInNjb3BlIjpbImFsbCJdLCJleHAiOjE2NjQyNTQ2NzIsImF1dGhvcml0aWVzIjpbInAxIl0sImp0aSI6Ijg4OTEyYjJkLTVkMDUtNGMxNC1iYmMzLWZkZTk5NzdmZWJjNiIsImNsaWVudF9pZCI6ImMxIn0.wkDBL7roLrvdBG2oGnXeoXq-zZRgE9IVV2nxd-ez_oA
```

JWT令牌由三部分组成，每部分中间使用点（.）分隔，比如：xxxxx.yyyyy.zzzzz
1.	**Header**        
  头部包括令牌的类型（即JWT）及使用的哈希算法（如HMAC SHA256或RSA）
  一个例子如下：
  下边是Header部分的内容
```JSON
   {
    "alg": "HS256",
    "typ": "JWT"
  }
  ```
  将上边的内容使用Base64Url编码，得到一个字符串就是JWT令牌的第一部分。
2.	 **Payload**
第二部分是负载，内容也是一个json对象，它是存放有效信息的地方，它可以存放jwt提供的信息字段，比如：iss（签发者）,exp（过期时间戳）, sub（面向的用户）等，也可自定义字段。
此部分不建议存放敏感信息，因为此部分可以解码还原原始内容。 最后将第二部分负载使用Base64Url编码，得到一个字符串就是JWT令牌的第二部分。
```JSON
  {
    "sub": "1234567890",
    "name": "456",
    "admin": true
  }
```
3.	 **Signature**
第三部分是签名，此部分用于防止jwt内容被篡改。这个部分使用base64url将前两部分进行编码，编码后使用点（.）连接组成字符串，最后使用header中声明的签名算法进行签名。
一个例子：

```JSON
HMACSHA256(
base64UrlEncode(header) + "." +
base64UrlEncode(payload),
secret)
```    
base64UrlEncode(header)：jwt令牌的第一部分。
base64UrlEncode(payload)：jwt令牌的第二部分。
secret：签名所使用的密钥。

为什么JWT可以防止篡改？
第三部分使用签名算法对第一部分和第二部分的内容进行签名，常用的签名算法是 HS256，常见的还有md5,sha 等，签名算法需要使用密钥进行签名，密钥不对外公开，并且签名是不可逆的，如果第三方更改了内容那么服务器验证签名就会失败，要想保证验证签名正确必须保证内容、密钥与签名前一致。


