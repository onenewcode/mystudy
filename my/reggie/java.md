# mybatisplus
## 结构和表的映射关系
EMyUserTable 对应表名为t_e_my_user_table;
## api
```java
@TableName：数据库表相关
@TableId：表主键标识
@TableField：表字段标识
@TableLogic：表字段逻辑处理注解（逻辑删除）
@TableField(exist = false)：表示该属性不为数据库表字段，但又是必须使用的。
@TableField(exist = true)：表示该属性为数据库表字段。
```
## 配置
### 分页
```java
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor(){
//        生成mybatisplus拦截器
        MybatisPlusInterceptor mybatisPlusInterceptor = new MybatisPlusInterceptor();
//为拦截器添加分页拦截插件
        mybatisPlusInterceptor.addInnerInterceptor(new PaginationInnerInterceptor());
        // 设置请求的页面大于最大页后操作， true调回到首页，false 继续请求  默认false
        // paginationInterceptor.setOverflow(false);
        // 设置最大单页限制数量，默认 500 条，-1 不受限制
        // paginationInterceptor.setLimit(500);
        // 开启 count 的 join 优化,只针对部分 left join
        return mybatisPlusInterceptor;
    }

```
# swagger
```xml
<!-- boot 3 -->
<dependency>
            <groupId>org.springdoc</groupId>
            <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
            <version>2.0.1</version>
        </dependency>
```
开箱即用无需配置
http://localhost:8080/swagger-ui/index.html