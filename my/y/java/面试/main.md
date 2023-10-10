# springboot
## SpringBoot接口开发的常用注解有哪些？

@Controller 标记此类是一个控制器，可以返回视图解析器指定的html页面，通过@ResponseBody可以将结果返回json、xml数据。

@RestController 相当于@ResponseBody加 @Controller，实现rest接口开发，返回json数据，不能返回html页面。

@RequestMapping 定义接口地址，可以标记在类上也可以标记在方法上，支持http的post、put、get等方法。

@PostMapping 定义post接口，只能标记在方法上，用于添加记录，复杂条件的查询接口。

@GetMapping 定义get接口，只能标记在方法上，用于查询接口的定义。

@PutMapping 定义put接口，只能标记在方法上，用于修改接口的定义。

@DeleteMapping 定义delete接口，只能标记在方法上，用于删除接口的定义。

@RequestBody 定义在方法上，用于将json串转成java对象。

@PathVarible 接收请求路径中占位符的值.

@ApiOperation swagger注解，对接口方法进行说明。

@Api wagger注解，对接口类进行说明。

@Autowired 基于类型注入。

@Resource 基于名称注入，如果基于名称注入失败转为基于类型注入。


# 项目
## 项目的开发流程是什么？

1、产品人员设计产品原型。

2、讨论需求。

3、分模块设计接口。

4、出接口文档。

5、将接口文档给到前端人员，前后端分离开发。

6、开发完毕进行测试。

7、测试完毕发布项目，由运维人员进行部署安装。