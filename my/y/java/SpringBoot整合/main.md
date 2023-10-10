# MinIO 
## 安装MinIo
```c
# 先创建minio 文件存放的位置
mkdir -p /opt/docker/minio/data

# 启动并指定端口
docker run \
  -p 9000:9000 \
  -p 5001:5001 \
  --name minio \
  -v /opt/docker/minio/data:/data \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadmin" \
  -d minio/minio server /data --console-address ":5001"
 
# 设置为和 docker 绑定启动,docker 启动则 minio 就启动
docker update --restart=always

```
## 导入依赖
```xml
<!-- https://mvnrepository.com/artifact/io.minio/minio -->
<dependency>
    <groupId>io.minio</groupId>
    <artifactId>minio</artifactId>
    <version>8.4.0</version>
</dependency>

```
## application.yml 配置信息
```yaml
minio:
  endpoint: http://192.168.218.131/:9000 #Minio服务所在地址
  bucketName: tulaoda #存储桶名称
  accessKey: minioadmin #访问的key
  secretKey: minioadmin #访问的秘钥
```
## MinioConfig.class配置类
```java
@Data
@Configuration
@ConfigurationProperties(prefix = "minio")
public class MinioConfig {

    private String endpoint;
    private String accessKey;
    private String secretKey;
    private String bucketName;

    @Bean
    public MinioClient minioClient() {
        return MinioClient.builder()
                .endpoint(endpoint)
                .credentials(accessKey, secretKey)
                .build();
    }
}
```
## minio工具类
```java
@Component
@Slf4j
public class MinioUtil {
    @Autowired
    private MinioConfig prop;

    @Resource
    private MinioClient minioClient;
    @Autowired
    private CodeService codeService;

    /**
     * 查看存储bucket是否存在
     * @return boolean
     */
    public Boolean bucketExists(String bucketName) {
        Boolean found;
        try {
            found = minioClient.bucketExists(BucketExistsArgs.builder().bucket(bucketName).build());
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
        return found;
    }

    /**
     * 创建存储bucket
     * @return Boolean
     */
    public Boolean makeBucket(String bucketName) {
        try {
            minioClient.makeBucket(MakeBucketArgs.builder()
                    .bucket(bucketName)
                    .build());
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }
    /**
     * 删除存储bucket
     * @return Boolean
     */
    public Boolean removeBucket(String bucketName) {
        try {
            minioClient.removeBucket(RemoveBucketArgs.builder()
                    .bucket(bucketName)
                    .build());
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }
    /**
     * 获取全部bucket
     */
    public List<Bucket> getAllBuckets() {
        try {
            List<Bucket> buckets = minioClient.listBuckets();
            return buckets;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }



    /**
     * 文件上传
     *
     * @param file 文件
     * @return Boolean
     */
    public String upload(MultipartFile file) {
        String originalFilename = file.getOriginalFilename();
        if (StringUtils.isBlank(originalFilename)){
            throw new RuntimeException();
        }
        String fileName = UuidUtils.generateUuid() + originalFilename.substring(originalFilename.lastIndexOf("."));
        String objectName = CommUtils.getNowDateLongStr("yyyy-MM/dd") + "/" + fileName;
        try {
            PutObjectArgs objectArgs = PutObjectArgs.builder().bucket(prop.getBucketName()).object(objectName)
                    .stream(file.getInputStream(), file.getSize(), -1).contentType(file.getContentType()).build();
            //文件名称相同会覆盖
            minioClient.putObject(objectArgs);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
        return objectName;
    }

    /**
     * 预览图片
     * @param fileName
     * @return
     */
    public String preview(String fileName){
        // 查看文件地址
        GetPresignedObjectUrlArgs build = new GetPresignedObjectUrlArgs().builder().bucket(prop.getBucketName()).object(fileName).method(Method.GET).build();
        try {
            String url = minioClient.getPresignedObjectUrl(build);
            return url;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * 文件下载
     * @param fileName 文件名称
     * @param res response
     * @return Boolean
     */
    public void download(String fileName, HttpServletResponse res) {
        GetObjectArgs objectArgs = GetObjectArgs.builder().bucket(prop.getBucketName())
                .object(fileName).build();
        try (GetObjectResponse response = minioClient.getObject(objectArgs)){
            byte[] buf = new byte[1024];
            int len;
            try (FastByteArrayOutputStream os = new FastByteArrayOutputStream()){
                while ((len=response.read(buf))!=-1){
                    os.write(buf,0,len);
                }
                os.flush();
                byte[] bytes = os.toByteArray();
                res.setCharacterEncoding("utf-8");
                // 设置强制下载不打开
                // res.setContentType("application/force-download");
                res.addHeader("Content-Disposition", "attachment;fileName=" + fileName);
                try (ServletOutputStream stream = res.getOutputStream()){
                    stream.write(bytes);
                    stream.flush();
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * 查看文件对象
     * @return 存储bucket内文件对象信息
     */
    public List<Item> listObjects() {
        Iterable<Result<Item>> results = minioClient.listObjects(
                ListObjectsArgs.builder().bucket(prop.getBucketName()).build());
        List<Item> items = new ArrayList<>();
        try {
            for (Result<Item> result : results) {
                items.add(result.get());
            }
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
        return items;
    }

    /**
     * 删除
     * @param fileName
     * @return
     * @throws Exception
     */
    public boolean remove(String fileName){
        try {
            minioClient.removeObject( RemoveObjectArgs.builder().bucket(prop.getBucketName()).object(fileName).build());
        }catch (Exception e){
            return false;
        }
        return true;
    }

}

```

## 文件处理接口
```java


@Api(tags = "文件相关接口")
@Slf4j
@RestController
@RequestMapping(value = "/product/file")
public class FileController {


    @Autowired
    private MinioUtil minioUtil;
    @Autowired
    private MinioConfig prop;

    @ApiOperation(value = "查看存储bucket是否存在")
    @GetMapping("/bucketExists")
    public R bucketExists(@RequestParam("bucketName") String bucketName) {
        return R.ok().put("bucketName",minioUtil.bucketExists(bucketName));
    }

    @ApiOperation(value = "创建存储bucket")
    @GetMapping("/makeBucket")
    public R makeBucket(String bucketName) {
        return R.ok().put("bucketName",minioUtil.makeBucket(bucketName));
    }

    @ApiOperation(value = "删除存储bucket")
    @GetMapping("/removeBucket")
    public R removeBucket(String bucketName) {
        return R.ok().put("bucketName",minioUtil.removeBucket(bucketName));
    }

    @ApiOperation(value = "获取全部bucket")
    @GetMapping("/getAllBuckets")
    public R getAllBuckets() {
        List<Bucket> allBuckets = minioUtil.getAllBuckets();
        return R.ok().put("allBuckets",allBuckets);
    }

    @ApiOperation(value = "文件上传返回url")
    @PostMapping("/upload")
    public R upload(@RequestParam("file") MultipartFile file) {
        String objectName = minioUtil.upload(file);
        if (null != objectName) {
            return R.ok().put("url",(prop.getEndpoint() + "/" + prop.getBucketName() + "/" + objectName));
        }
        return R.error();
    }

    @ApiOperation(value = "图片/视频预览")
    @GetMapping("/preview")
    public R preview(@RequestParam("fileName") String fileName) {
        return R.ok().put("filleName",minioUtil.preview(fileName));
    }

    @ApiOperation(value = "文件下载")
    @GetMapping("/download")
    public R download(@RequestParam("fileName") String fileName, HttpServletResponse res) {
        minioUtil.download(fileName,res);
        return R.ok();
    }

    @ApiOperation(value = "删除文件", notes = "根据url地址删除文件")
    @PostMapping("/delete")
    public R remove(String url) {
        String objName = url.substring(url.lastIndexOf(prop.getBucketName()+"/") + prop.getBucketName().length()+1);
        minioUtil.remove(objName);
        return R.ok().put("objName",objName);
    }

}

```
# jwt
## 环境准备
JWT依赖
```xml
<!--        jwt 依赖-->
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt</artifactId>
    <version>0.9.1</version>
</dependency>

<!--另一种token插件 性能更高-->
<dependency>
    <groupId>com.auth0</groupId>
    <artifactId>java-jwt</artifactId>
    <version>3.10.3</version>
</dependency>
```


##  生成token工具类
```java
import io.jsonwebtoken.*;
import org.springframework.util.StringUtils;

import java.util.Date;

public class JwtHelper {

    // token 失效时间  当前设置过期时间 24小时
    private static long tokenExpiration = 24*60*60*1000;

    //生成token 的私有盐 这个按道理来说只有自己知道 加密的时候加入盐 token就不会轻易的被破解
    private static String tokenSignKey = "123456";

    /**
     * 生成jwt令牌【token】 也可以根据别的用户信息生成token 这里选择了 userId userName
     * @param userId  用户id
     * @param userName  用户名
     * @return
     */
    public static String createToken(Long userId,String userName){
          String token =  Jwts.builder()

                  //公共部分
                  .setSubject("YYGH-USER")
                  //设置token 的过期时间
                  .setExpiration(new Date(System.currentTimeMillis()+tokenExpiration))

                  //私有部分 
                  .claim("userId",userId)
                  .claim("userName",userName)

                  //签名部分 设置加密算法 + 自己的盐
                  .signWith(SignatureAlgorithm.HS512,tokenSignKey)

                  //对token的压缩方法 载荷过长可以进行压缩
                  .compressWith(CompressionCodecs.GZIP)
                  .compact();

          return token;
    }

    /**
     * 根据token 得到用户ID
     * @param token
     * @return
     */
    public static Long getUserIdByToken(String token){

        //判断token是否 null
        if(StringUtils.isEmpty(token)) return null;

        /**
         * 根据自定义的盐值解析token 获取token里面私有部分的信息
         *
         * tokenSignKey 自己设置的盐
         * token  传过来的token
         */
        Jws<Claims> claimsJwts =  Jwts.parser().setSigningKey(tokenSignKey).parseClaimsJws(token);

        //私有部分的数据体
        Claims jwtsBody = claimsJwts.getBody();
        Long userId = (Long) jwtsBody.get("userId");
        return userId;
    }

    /**
     * 根据token 获取用户名称
     * @param token
     * @return
     */
    public static String getUserNameByToken(String token){
        if(StringUtils.isEmpty(token)) return "";
        Jws<Claims> claimsJws
                = Jwts.parser().setSigningKey(tokenSignKey).parseClaimsJws(token);
        Claims claims = claimsJws.getBody();
        return (String)claims.get("userName");
    }

```
