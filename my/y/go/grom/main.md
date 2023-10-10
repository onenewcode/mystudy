# 入门
## 模型定义
模型一般都是普通的 Golang 的结构体，Go的基本数据类型，或者指针。sql.Scanner 和 driver.Valuer，同时也支持接口。

例子：
```go
type User struct {
  gorm.Model
  Name         string
  Age          sql.NullInt64
  Birthday     *time.Time
  Email        string  `gorm:"type:varchar(100);unique_index"`
  Role         string  `gorm:"size:255"` //设置字段的大小为255个字节
  MemberNumber *string `gorm:"unique;not null"` // 设置 memberNumber 字段唯一且不为空
  Num          int     `gorm:"AUTO_INCREMENT"` // 设置 Num字段自增
  Address      string  `gorm:"index:addr"` // 给Address 创建一个名字是  `addr`的索引
  IgnoreMe     int     `gorm:"-"` //忽略这个字段
}
```
## 惯例
### gorm.Model
gorm.Model 是一个包含一些基本字段的结构体, 包含的字段有 ID，CreatedAt， UpdatedAt， DeletedAt。

你可以用它来嵌入到你的模型中，或者也可以用它来建立自己的模型。
```go
// gorm.Model 定义
type Model struct {
  ID        uint `gorm:"primary_key"`
  CreatedAt time.Time
  UpdatedAt time.Time
  DeletedAt *time.Time
}

// 将字段 `ID`, `CreatedAt`, `UpdatedAt`, `DeletedAt` 注入到 `User` 模型中
type User struct {
  gorm.Model
  Name string
}

// 声明 gorm.Model 模型
type User struct {
  ID   int
  Name string
}
```
### ID 作为主键
GORM 默认使用 ID 作为主键名。
```go
type User struct {
  ID   string // 字段名 `ID` 将被作为默认的主键名
}

// 设置字段 `AnimalID` 为默认主键
type Animal struct {
  AnimalID int64 `gorm:"primary_key"`
  Name     string
  Age      int64
}
```
### 复数表名
表名是结构体名称的复数形式
```go
type User struct {} // 默认的表名是 `users`

// 设置 `User` 的表名为 `profiles`
func (User) TableName() string {
  return "profiles"
}

func (u User) TableName() string {
    if u.Role == "admin" {
        return "admin_users"
    } else {
        return "users"
    }
}


// 如果设置禁用表名复数形式属性为 true，`User` 的表名将是 `user`
db.SingularTable(true)
```
### 指定表名
```go
// 用 `User` 结构体创建 `delete_users` 表
db.Table("deleted_users").CreateTable(&User{})

var deleted_users []User
db.Table("deleted_users").Find(&deleted_users)
//// SELECT * FROM deleted_users;

db.Table("deleted_users").Where("name = ?", "jinzhu").Delete()
//// DELETE FROM deleted_users WHERE name = 'jinzhu';
```
### 修改默认表名
你可以通过定义 DefaultTableNameHandler 字段来对表名使用任何规则。
```go
gorm.DefaultTableNameHandler = func (db *gorm.DB, defaultTableName string) string  {
    return "prefix_" + defaultTableName;
}
```
### 蛇形列名
列名是字段名的蛇形小写形式
```go
type User struct {
  ID        uint      // 字段名是 `id`
  Name      string    // 字段名是 `name`
  Birthday  time.Time // 字段名是 `birthday`
  CreatedAt time.Time // 字段名是 `created_at`
}

// 重写列名
type Animal struct {
    AnimalId    int64     `gorm:"column:beast_id"`         // 设置列名为 `beast_id`
    Birthday    time.Time `gorm:"column:day_of_the_beast"` // 设置列名为 `day_of_the_beast`
    Age         int64     `gorm:"column:age_of_the_beast"` // 设置列名为 `age_of_the_beast`
}
```
### 时间戳跟踪
CreatedAt
对于有 CreatedAt 字段的模型，它将被设置为首次创建记录的当前时间。
```go
db.Create(&user) // 将设置 `CreatedAt` 为当前时间

// 你可以使用 `Update` 方法来更改默认时间
db.Model(&user).Update("CreatedAt", time.Now())
```

### Up datedAt
对于有 UpdatedAt 字段的模型，它将被设置为记录更新时的当前时间。
```go
db.Save(&user) // 将设置 `UpdatedAt` 为当前时间

db.Model(&user).Update("name", "jinzhu") // 将设置 `UpdatedAt` 为当前时间
```
### DeletedAt
对于有 DeletedAt 字段的模型，当删除它们的实例时，它们并没有被从数据库中删除，只是将 DeletedAt 字段设置为当前时间。
# CRUD接口
## 创建
### 创建记录
```go
user := User{Name: "Jinzhu", Age: 18, Birthday: time.Now()}

db.NewRecord(user) // => 返回 `true` ，因为主键为空

db.Create(&user)

db.NewRecord(user) // => 在 `user` 之后创建返回 `false`
```
### 默认值
你可以通过标签定义字段的默认值，例如：
```go
type Animal struct {
    ID   int64
    Name string `gorm:"default:'galeone'"`
    Age  int64
}-
```
然后 SQL 会排除那些没有值或者有 零值 的字段，在记录插入数据库之后，gorm将从数据库中加载这些字段的值。
```go
var animal = Animal{Age: 99, Name: ""}
db.Create(&animal)
// INSERT INTO animals("age") values('99');
// SELECT name from animals WHERE ID=111; // 返回的主键是 111
// animal.Name => 'galeone'
```
注意 所有包含零值的字段，像 0，''，false 或者其他的 零值 不会被保存到数据库中，但会使用这个字段的默认值。你应该考虑使用指针类型或者其他的值来避免这种情况:
```go
// Use pointer value
type User struct {
  gorm.Model
  Name string
  Age  *int `gorm:"default:18"`
}

// Use scanner/valuer
type User struct {
  gorm.Model
  Name string
  Age  sql.NullInt64 `gorm:"default:18"`
}
```
### 在钩子中设置字段值
如果你想在 BeforeCreate 函数中更新字段的值，应该使用 scope.SetColumn，例如：
```go
func (user *User) BeforeCreate(scope *gorm.Scope) error {
  scope.SetColumn("ID", uuid.New())
  return nil
}
```
### 创建额外选项
```go
// 为插入 SQL 语句添加额外选项
db.Set("gorm:insert_option", "ON CONFLICT").Create(&product)
// INSERT INTO products (name, code) VALUES ("name", "code") ON CONFLICT;
```
## 查询
### 查询
```go
// 获取第一条记录，按主键排序
db.First(&user)
//// SELECT * FROM users ORDER BY id LIMIT 1;

// 获取一条记录，不指定排序
db.Take(&user)
//// SELECT * FROM users LIMIT 1;

// 获取最后一条记录，按主键排序
db.Last(&user)
//// SELECT * FROM users ORDER BY id DESC LIMIT 1;

// 获取所有的记录
db.Find(&users)
//// SELECT * FROM users;

// 通过主键进行查询 (仅适用于主键是数字类型)
db.First(&user, 10)
//// SELECT * FROM users WHERE id = 10;
```
### Where
```go
// 获取第一条匹配的记录
db.Where("name = ?", "jinzhu").First(&user)
//// SELECT * FROM users WHERE name = 'jinzhu' limit 1;

// 获取所有匹配的记录
db.Where("name = ?", "jinzhu").Find(&users)
//// SELECT * FROM users WHERE name = 'jinzhu';

// <>
db.Where("name <> ?", "jinzhu").Find(&users)

// IN
db.Where("name in (?)", []string{"jinzhu", "jinzhu 2"}).Find(&users)

// LIKE
db.Where("name LIKE ?", "%jin%").Find(&users)

// AND
db.Where("name = ? AND age >= ?", "jinzhu", "22").Find(&users)

// Time
db.Where("updated_at > ?", lastWeek).Find(&users)

// BETWEEN
db.Where("created_at BETWEEN ? AND ?", lastWeek, today).Find(&users)
```
### Struct & Map
```go
// Struct
db.Where(&User{Name: "jinzhu", Age: 20}).First(&user)
//// SELECT * FROM users WHERE name = "jinzhu" AND age = 20 LIMIT 1;

// Map
db.Where(map[string]interface{}{"name": "jinzhu", "age": 20}).Find(&users)
//// SELECT * FROM users WHERE name = "jinzhu" AND age = 20;

// 多主键 slice 查询
db.Where([]int64{20, 21, 22}).Find(&users)
//// SELECT * FROM users WHERE id IN (20, 21, 22);
```
当通过struct进行查询的时候，GORM 将会查询这些字段的非零值， 意味着你的字段包含 0， ''， false 或者其他 零值, 将不会出现在查询语句中， 例如:
```go
db.Where(&User{Name: "jinzhu", Age: 0}).Find(&users)
//// SELECT * FROM users WHERE name = "jinzhu";
```

你可以考虑适用指针类型或者 scanner/valuer 来避免这种情况。
```go
// 使用指针类型
type User struct {
  gorm.Model
  Name string
  Age  *int
}

// 使用 scanner/valuer
type User struct {
  gorm.Model
  Name string
  Age  sql.NullInt64
}
```
### Not
和 Where查询类似
```go
db.Not("name", "jinzhu").First(&user)
//// SELECT * FROM users WHERE name <> "jinzhu" LIMIT 1;

// 不包含
db.Not("name", []string{"jinzhu", "jinzhu 2"}).Find(&users)
//// SELECT * FROM users WHERE name NOT IN ("jinzhu", "jinzhu 2");

//不在主键 slice 中
db.Not([]int64{1,2,3}).First(&user)
//// SELECT * FROM users WHERE id NOT IN (1,2,3);

db.Not([]int64{}).First(&user)
//// SELECT * FROM users;

// 原生 SQL
db.Not("name = ?", "jinzhu").First(&user)
//// SELECT * FROM users WHERE NOT(name = "jinzhu");

// Struct
db.Not(User{Name: "jinzhu"}).First(&user)
//// SELECT * FROM users WHERE name <> "jinzhu";
```
### Or
```go
db.Where("role = ?", "admin").Or("role = ?", "super_admin").Find(&users)
//// SELECT * FROM users WHERE role = 'admin' OR role = 'super_admin';

// Struct
db.Where("name = 'jinzhu'").Or(User{Name: "jinzhu 2"}).Find(&users)
//// SELECT * FROM users WHERE name = 'jinzhu' OR name = 'jinzhu 2';

// Map
db.Where("name = 'jinzhu'").Or(map[string]interface{}{"name": "jinzhu 2"}).Find(&users)
//// SELECT * FROM users WHERE name = 'jinzhu' OR name = 'jinzhu 2';
```
### 行内条件查询
和 Where 查询类似。

需要注意的是，当使用链式调用传入行内条件查询时，这些查询不会被传参给后续的中间方法。
```go
// 通过主键进行查询 (仅适用于主键是数字类型)
db.First(&user, 23)
//// SELECT * FROM users WHERE id = 23 LIMIT 1;
// 非数字类型的主键查询
db.First(&user, "id = ?", "string_primary_key")
//// SELECT * FROM users WHERE id = 'string_primary_key' LIMIT 1;

// 原生 SQL
db.Find(&user, "name = ?", "jinzhu")
//// SELECT * FROM users WHERE name = "jinzhu";

db.Find(&users, "name <> ? AND age > ?", "jinzhu", 20)
//// SELECT * FROM users WHERE name <> "jinzhu" AND age > 20;

// Struct
db.Find(&users, User{Age: 20})
//// SELECT * FROM users WHERE age = 20;

// Map
db.Find(&users, map[string]interface{}{"age": 20})
//// SELECT * FROM users WHERE age = 20;
```
### 额外的查询选项
```go
// 为查询 SQL 添加额外的选项
db.Set("gorm:query_option", "FOR UPDATE").First(&user, 10)
//// SELECT * FROM users WHERE id = 10 FOR UPDATE;
```
### FirstOrInit
获取第一条匹配的记录，或者通过给定的条件下初始一条新的记录（仅适用与于 struct 和 map 条件）。
```go
// 未查询到
db.FirstOrInit(&user, User{Name: "non_existing"})
//// user -> User{Name: "non_existing"}

// 查询到
db.Where(User{Name: "Jinzhu"}).FirstOrInit(&user)
//// user -> User{Id: 111, Name: "Jinzhu", Age: 20}
db.FirstOrInit(&user, map[string]interface{}{"name": "jinzhu"})
//// user -> User{Id: 111, Name: "Jinzhu", Age: 20}
```
### Attrs
如果未找到记录，则使用参数初始化 struct
```go
// 未查询到
db.Where(User{Name: "non_existing"}).Attrs(User{Age: 20}).FirstOrInit(&user)
//// SELECT * FROM USERS WHERE name = 'non_existing';
//// user -> User{Name: "non_existing", Age: 20}

db.Where(User{Name: "non_existing"}).Attrs("age", 20).FirstOrInit(&user)
//// SELECT * FROM USERS WHERE name = 'non_existing';
//// user -> User{Name: "non_existing", Age: 20}

// 查询到
db.Where(User{Name: "Jinzhu"}).Attrs(User{Age: 30}).FirstOrInit(&user)
//// SELECT * FROM USERS WHERE name = jinzhu';
//// user -> User{Id: 111, Name: "Jinzhu", Age: 20}
```
### Assign
无论是否查询到数据，都将参数赋值给 struct
```go
// 未查询到
db.Where(User{Name: "non_existing"}).Assign(User{Age: 20}).FirstOrInit(&user)
//// user -> User{Name: "non_existing", Age: 20}

// 查询到
db.Where(User{Name: "Jinzhu"}).Assign(User{Age: 30}).FirstOrInit(&user)
//// SELECT * FROM USERS WHERE name = jinzhu';
//// user -> User{Id: 111, Name: "Jinzhu", Age: 30}
FirstOrCreate
获取第一条匹配的记录，或者通过给定的条件创建一条记录 （仅适用与于 struct 和 map 条件）。

// 未查询到
db.FirstOrCreate(&user, User{Name: "non_existing"})
//// INSERT INTO "users" (name) VALUES ("non_existing");
//// user -> User{Id: 112, Name: "non_existing"}

// 查询到
db.Where(User{Name: "Jinzhu"}).FirstOrCreate(&user)
//// user -> User{Id: 111, Name: "Jinzhu"}
```
e
## 高级查询
### 子查询
#### 使用 *gorm.expr 进行子查询
```go
db.Where("amount > ?", DB.Table("orders").Select("AVG(amount)").Where("state = ?", "paid").QueryExpr()).Find(&orders)
// SELECT * FROM "orders"  WHERE "orders"."deleted_at" IS NULL AND (amount > (SELECT AVG(amount) FROM "orders"  WHERE (state = 'paid')));
```
### 查询
指定要从数据库检索的字段，默认情况下，将选择所有字段。
```go
db.Select("name, age").Find(&users)
//// SELECT name, age FROM users;

db.Select([]string{"name", "age"}).Find(&users)
//// SELECT name, age FROM users;

db.Table("users").Select("COALESCE(age,?)", 42).Rows()
//// SELECT COALESCE(age,'42') FROM users;
```
### Order
使用 Order 从数据库查询记录时，当第二个参数设置为 true 时，将会覆盖之前的定义条件。
```go
db.Order("age desc, name").Find(&users)
//// SELECT * FROM users ORDER BY age desc, name;

// 多个排序条件
db.Order("age desc").Order("name").Find(&users)
//// SELECT * FROM users ORDER BY age desc, name;

// 重新排序
db.Order("age desc").Find(&users1).Order("age", true).Find(&users2)
//// SELECT * FROM users ORDER BY age desc; (users1)
//// SELECT * FROM users ORDER BY age; (users2)
```
### Limit
指定要查询的最大记录数
```go
db.Limit(3).Find(&users)
//// SELECT * FROM users LIMIT 3;

// 用 -1 取消 LIMIT 限制条件
db.Limit(10).Find(&users1).Limit(-1).Find(&users2)
//// SELECT * FROM users LIMIT 10; (users1)
//// SELECT * FROM users; (users2)
```
### Offset
指定在开始返回记录之前要跳过的记录数。
```go
db.Offset(3).Find(&users)
//// SELECT * FROM users OFFSET 3;

// 用 -1 取消 OFFSET 限制条件
db.Offset(10).Find(&users1).Offset(-1).Find(&users2)
//// SELECT * FROM users OFFSET 10; (users1)
//// SELECT * FROM users; (users2)
```
### Count
获取模型记录数
```go
db.Where("name = ?", "jinzhu").Or("name = ?", "jinzhu 2").Find(&users).Count(&count)
//// SELECT * from USERS WHERE name = 'jinzhu' OR name = 'jinzhu 2'; (users)
//// SELECT count(*) FROM users WHERE name = 'jinzhu' OR name = 'jinzhu 2'; (count)

db.Model(&User{}).Where("name = ?", "jinzhu").Count(&count)
//// SELECT count(*) FROM users WHERE name = 'jinzhu'; (count)

db.Table("deleted_users").Count(&count)
//// SELECT count(*) FROM deleted_users;
```
注意： 在查询链中使用 Count 时，必须放在最后一个位置，因为它会覆盖 SELECT 查询条件。

### Group 和 Having
```go
rows, err := db.Table("orders").Select("date(created_at) as date, sum(amount) as total").Group("date(created_at)").Rows()
for rows.Next() {
    ...
}

rows, err := db.Table("orders").Select("date(created_at) as date, sum(amount) as total").Group("date(created_at)").Having("sum(amount) > ?", 100).Rows()
for rows.Next() {
    ...
}

type Result struct {
    Date  time.Time
    Total int64
}
db.Table("orders").Select("date(created_at) as date, sum(amount) as total").Group("date(created_at)").Having("sum(amount) > ?", 100).Scan(&results)
```
### Joins
指定关联条件
```go
rows, err := db.Table("users").Select("users.name, emails.email").Joins("left join emails on emails.user_id = users.id").Rows()
for rows.Next() {
    ...
}

db.Table("users").Select("users.name, emails.email").Joins("left join emails on emails.user_id = users.id").Scan(&results)

// 多个关联查询
db.Joins("JOIN emails ON emails.user_id = users.id AND emails.email = ?", "jinzhu@example.org").Joins("JOIN credit_cards ON credit_cards.user_id = users.id").Where("credit_cards.number = ?", "411111111111").Find(&user)
```
### Pluck
使用 Pluck 从模型中查询单个列作为集合。如果想查询多个列，应该使用 Scan 代替。
```go
var ages []int64
db.Find(&users).Pluck("age", &ages)

var names []string
db.Model(&User{}).Pluck("name", &names)

db.Table("deleted_users").Pluck("name", &names)

// Requesting more than one column? Do it like this:
db.Select("name, age").Find(&users)
```
### Scan
将 Scan 查询结果放入另一个结构体中。
```go
type Result struct {
    Name string
    Age  int
}

var result Result
db.Table("users").Select("name, age").Where("name = ?", 3).Scan(&result)

// Raw SQL
db.Raw("SELECT name, age FROM users WHERE name = ?", 3).Scan(&result)
```

## 更新
### 更新所有字段
Save 方法在执行 SQL 更新操作时将包含所有字段，即使这些字段没有被修改。
```go
db.First(&user)

user.Name = "jinzhu 2"
user.Age = 100
db.Save(&user)

//// UPDATE users SET name='jinzhu 2', age=100, birthday='2016-01-01', updated_at = '2013-11-17 21:34:10' WHERE id=111;
```
### 更新已更改的字段
如果你只想更新已经修改了的字段，可以使用 Update，Updates 方法。
```go
// 如果单个属性被更改了，更新它
db.Model(&user).Update("name", "hello")
//// UPDATE users SET name='hello', updated_at='2013-11-17 21:34:10' WHERE id=111;

// 使用组合条件更新单个属性
db.Model(&user).Where("active = ?", true).Update("name", "hello")
//// UPDATE users SET name='hello', updated_at='2013-11-17 21:34:10' WHERE id=111 AND active=true;

// 使用 `map` 更新多个属性，只会更新那些被更改了的字段
db.Model(&user).Updates(map[string]interface{}{"name": "hello", "age": 18, "actived": false})
//// UPDATE users SET name='hello', age=18, actived=false, updated_at='2013-11-17 21:34:10' WHERE id=111;

// 使用 `struct` 更新多个属性，只会更新那些被修改了的和非空的字段
db.Model(&user).Updates(User{Name: "hello", Age: 18})
//// UPDATE users SET name='hello', age=18, updated_at = '2013-11-17 21:34:10' WHERE id = 111;

// 警告： 当使用结构体更新的时候, GORM 只会更新那些非空的字段
// 例如下面的更新，没有东西会被更新，因为像 "", 0, false 是这些字段类型的空值
db.Model(&user).Updates(User{Name: "", Age: 0, Actived: false})
```
### 更新选中的字段
如果你在执行更新操作时只想更新或者忽略某些字段，可以使用 Select，Omit方法。
```go
db.Model(&user).Select("name").Updates(map[string]interface{}{"name": "hello", "age": 18, "actived": false})
//// UPDATE users SET name='hello', updated_at='2013-11-17 21:34:10' WHERE id=111;

db.Model(&user).Omit("name").Updates(map[string]interface{}{"name": "hello", "age": 18, "actived": false})
//// UPDATE users SET age=18, actived=false, updated_at='2013-11-17 21:34:10' WHERE id=111;
```
### 更新列钩子方法
上面的更新操作更新时会执行模型的 BeforeUpdate 和 AfterUpdate 方法，来更新 UpdatedAt 时间戳，并且保存他的 关联。如果你不想执行这些操作，可以使用 UpdateColumn，UpdateColumns 方法。
```go
// Update single attribute, similar with `Update`
db.Model(&user).UpdateColumn("name", "hello")
//// UPDATE users SET name='hello' WHERE id = 111;

// Update multiple attributes, similar with `Updates`
db.Model(&user).UpdateColumns(User{Name: "hello", Age: 18})
//// UPDATE users SET name='hello', age=18 WHERE id = 111;
```
### 批量更新
批量更新时，钩子函数不会执行
```go
db.Table("users").Where("id IN (?)", []int{10, 11}).Updates(map[string]interface{}{"name": "hello", "age": 18})
//// UPDATE users SET name='hello', age=18 WHERE id IN (10, 11);

// 使用结构体更新将只适用于非零值，或者使用 map[string]interface{}
db.Model(User{}).Updates(User{Name: "hello", Age: 18})
//// UPDATE users SET name='hello', age=18;

// 使用 `RowsAffected` 获取更新影响的记录数
db.Model(User{}).Updates(User{Name: "hello", Age: 18}).RowsAffected
```
### 带有表达式的 SQL 更新
```go
DB.Model(&product).Update("price", gorm.Expr("price * ? + ?", 2, 100))
//// UPDATE "products" SET "price" = price * '2' + '100', "updated_at" = '2013-11-17 21:34:10' WHERE "id" = '2';

DB.Model(&product).Updates(map[string]interface{}{"price": gorm.Expr("price * ? + ?", 2, 100)})
//// UPDATE "products" SET "price" = price * '2' + '100', "updated_at" = '2013-11-17 21:34:10' WHERE "id" = '2';

DB.Model(&product).UpdateColumn("quantity", gorm.Expr("quantity - ?", 1))
//// UPDATE "products" SET "quantity" = quantity - 1 WHERE "id" = '2';

DB.Model(&product).Where("quantity > 1").UpdateColumn("quantity", gorm.Expr("quantity - ?", 1))
//// UPDATE "products" SET "quantity" = quantity - 1 WHERE "id" = '2' AND quantity > 1;
```
### 在钩子函数中更新值
如果你想使用 BeforeUpdate、BeforeSave钩子函数修改更新的值，可以使用 scope.SetColumn方法，例如：
```go
func (user *User) BeforeSave(scope *gorm.Scope) (err error) {
  if pw, err := bcrypt.GenerateFromPassword(user.Password, 0); err == nil {
    scope.SetColumn("EncryptedPassword", pw)
  }
}
```
### 额外的更新选项
```go
// 在更新 SQL 语句中添加额外的 SQL 选项
db.Model(&user).Set("gorm:update_option", "OPTION (OPTIMIZE FOR UNKNOWN)").Update("name", "hello")
//// UPDATE users SET name='hello', updated_at = '2013-11-17 21:34:10' WHERE id=111 OPTION (OPTIMIZE FOR UNKNOWN);
```
## 删除
### 删除记录
警告：当删除一条记录的时候，你需要确定这条记录的主键有值，GORM会使用主键来删除这条记录。如果主键字段为空，GORM会删除模型中所有的记录。
```go
// 删除一条存在的记录
db.Delete(&email)
//// DELETE from emails where id=10;

// 为删除 SQL 语句添加额外选项
db.Set("gorm:delete_option", "OPTION (OPTIMIZE FOR UNKNOWN)").Delete(&email)
//// DELETE from emails where id=10 OPTION (OPTIMIZE FOR UNKNOWN);
```
### 批量删除
删除所有匹配的记录
```go
db.Where("email LIKE ?", "%jinzhu%").Delete(Email{})
//// DELETE from emails where email LIKE "%jinzhu%";

db.Delete(Email{}, "email LIKE ?", "%jinzhu%")
//// DELETE from emails where email LIKE "%jinzhu%";
```
### 软删除
如果模型中有 DeletedAt 字段，它将自动拥有软删除的能力！当执行删除操作时，数据并不会永久的从数据库中删除，而是将 DeletedAt 的值更新为当前时间。
```go
db.Delete(&user)
//// UPDATE users SET deleted_at="2013-10-29 10:23" WHERE id = 111;

// 批量删除
db.Where("age = ?", 20).Delete(&User{})
//// UPDATE users SET deleted_at="2013-10-29 10:23" WHERE age = 20;

// 在查询记录时，软删除记录会被忽略
db.Where("age = 20").Find(&user)
//// SELECT * FROM users WHERE age = 20 AND deleted_at IS NULL;

// 使用 Unscoped 方法查找软删除记录
db.Unscoped().Where("age = 20").Find(&users)
//// SELECT * FROM users WHERE age = 20;
```
# 关联
## Belongs To
### 属于
belongs to 关联建立一个和另一个模型的一对一连接，使得模型声明每个实例都「属于」另一个模型的一个实例 。

例如，如果你的应用包含了用户和用户资料， 并且每一个用户资料只分配给一个用户
```go
type User struct {
  gorm.Model
  Name string
}

// `Profile` 属于 `User`， `UserID` 是外键
type Profile struct {
  gorm.Model
  UserID int
  User   User
  Name   string
}
```
### 外键
为了定义从属关系， 外键是必须存在的， 默认的外键使用所有者类型名称加上其主键。

像上面的例子，为了声明一个模型属于 User，它的外键应该为 UserID。

GORM 提供了一个定制外键的方法，例如:
```go
type User struct {
    gorm.Model
    Name string
}

type Profile struct {
    gorm.Model
  Name      string
  User      User `gorm:"foreignkey:UserRefer"` // 使用 UserRefer 作为外键
  UserRefer string
}
```
### 关联外键
对于从属关系， GORM 通常使用所有者的主键作为外键值，在上面的例子中，就是 User 的 ID。

当你分配一个资料给一个用户， GORM 将保存用户表的 ID 值 到 用户资料表的 UserID 字段里。

你可以通过改变标签 association_foreignkey 来改变它， 例如：
```go
type User struct {
    gorm.Model
  Refer int
    Name string
}

type Profile struct {
    gorm.Model
  Name      string
  User      User `gorm:"association_foreignkey:Refer"` // use Refer 作为关联外键
  UserRefer string
}
```
### 使用属于
你能找到 belongs to 和 Related 的关联
```go
db.Model(&user).Related(&profile)
//// SELECT * FROM profiles WHERE user_id = 111; // 111 is user's ID
```

## Has One
has one 关联也是与另一个模型建立一对一的连接，但语义（和结果）有些不同。 此关联表示模型的每个实例包含或拥有另一个模型的一个实例。

例如，如果你的应用程序包含用户和信用卡，并且每个用户只能有一张信用卡。
```go
// 用户有一个信用卡，CredtCardID 外键
type User struct {
    gorm.Model
    CreditCard   CreditCard
}

type CreditCard struct {
    gorm.Model
    Number   string
    UserID    uint
}
```
### 外键
对于一对一关系，一个外键字段也必须存在，所有者将保存主键到模型关联的字段里。

这个字段的名字通常由 belongs to model 的类型加上它的 primary key 产生的，就上面的例子而言，它就是 CreditCardID

当你给用户一个信用卡， 它将保存一个信用卡的 ID 到 CreditCardID 字段中。

如果你想使用另一个字段来保存这个关系，你可以通过使用标签 foreignkey 来改变它， 例如：
```go
type User struct {
  gorm.Model
  CreditCard CreditCard `gorm:"foreignkey:CardRefer"`
}

type CreditCard struct {
    gorm.Model
    Number      string
    UserName string
}
```
### 关联外键
通常，所有者会保存 belogns to model 的主键到外键，你可以改为保存其他字段， 就像下面的例子使用 Number 。
```go
type User struct {
  gorm.Model
  CreditCard CreditCard `gorm:"association_foreignkey:Number"`
}

type CreditCard struct {
    gorm.Model
    Number string
    UID       string
}
```
### 多态关联
支持多态的一对多和一对一关联。
```go
  type Cat struct {
    ID    int
    Name  string
    Toy   Toy `gorm:"polymorphic:Owner;"`
  }

  type Dog struct {
    ID   int
    Name string
    Toy  Toy `gorm:"polymorphic:Owner;"`
  }

  type Toy struct {
    ID        int
    Name      string
    OwnerID   int
    OwnerType string
  }
  ```
注意：多态属于和多对多是明确的不支持并将会抛出错误。

### 使用一对一
你可以通过 Related 找到 has one 关联。
```go
var card CreditCard
db.Model(&user).Related(&card, "CreditCard")
//// SELECT * FROM credit_cards WHERE user_id = 123; // 123 是用户表的主键
// CreditCard  是用户表的字段名，这意味着获取用户的信用卡关系并写入变量 card。
// 像上面的例子，如果字段名和变量类型名一样，它就可以省略， 像：
db.Model(&user).Related(&card)
```
## Has Many
### 一对多
has many 关联就是创建和另一个模型的一对多关系， 不像 has one，所有者可以拥有0个或多个模型实例。

例如，如果你的应用包含用户和信用卡， 并且每一个用户都拥有多张信用卡。
```go
// 用户有多张信用卡，UserID 是外键
type User struct {
    gorm.Model
    CreditCards []CreditCard
}

type CreditCard struct {
    gorm.Model
    Number   string
    UserID  uint
}
```
### 外键
为了定义一对多关系， 外键是必须存在的，默认外键的名字是所有者类型的名字加上它的主键。

就像上面的例子，为了定义一个属于User 的模型，外键就应该为 UserID。

使用其他的字段名作为外键， 你可以通过 foreignkey 来定制它， 例如:
```go
type User struct {
    gorm.Model
    CreditCards []CreditCard `gorm:"foreignkey:UserRefer"`
}

type CreditCard struct {
    gorm.Model
    Number    string
  UserRefer uint
}
```
### 外键关联
GORM 通常使用所有者的主键作为外键的值， 在上面的例子中，它就是 User 的 ID。

当你分配信用卡给一个用户， GORM 将保存用户 ID 到信用卡表的 UserID 字段中。

你能通过 association_foreignkey 来改变它， 例如:
```go
type User struct {
    gorm.Model
  MemberNumber string
    CreditCards  []CreditCard `gorm:"foreignkey:UserMemberNumber;association_foreignkey:MemberNumber"`
}

type CreditCard struct {
    gorm.Model
    Number           string
  UserMemberNumber string
}
```
### 多态关联
支持多态的一对多和一对一关联。
```go
  type Cat struct {
    ID    int
    Name  string
    Toy   []Toy `gorm:"polymorphic:Owner;"`
  }

  type Dog struct {
    ID   int
    Name string
    Toy  []Toy `gorm:"polymorphic:Owner;"`
  }

  type Toy struct {
    ID        int
    Name      string
    OwnerID   int
    OwnerType string
  }
  ```
注意：多态属于和多对多是明确不支持并会抛出错误的。

### 使用一对多
你可以通过Related 找到 has many 关联关系。
```go
db.Model(&user).Related(&emails)
//// SELECT * FROM emails WHERE user_id = 111; // 111 是用户表的主键
```
## Many To Many
### 多对多
多对多为两个模型增加了一个中间表。

例如，如果你的应用包含用户和语言， 一个用户会说多种语言，并且很多用户会说一种特定的语言。
```go
// 用户拥有并属于多种语言， 使用  `user_languages` 作为中间表
type User struct {
    gorm.Model
    Languages         []Language `gorm:"many2many:user_languages;"`
}

type Language struct {
    gorm.Model
    Name string
}
```
### 反向关联
```go
// 用户拥有并且属于多种语言，使用 `user_languages` 作为中间表
type User struct {
    gorm.Model
    Languages         []*Language `gorm:"many2many:user_languages;"`
}

type Language struct {
    gorm.Model
    Name string
    Users               []*User     `gorm:"many2many:user_languages;"`
}

db.Model(&language).Related(&users)
//// SELECT * FROM "users" INNER JOIN "user_languages" ON "user_languages"."user_id" = "users"."id" WHERE  ("user_languages"."language_id" IN ('111'))
```
### 外键
```go
type CustomizePerson struct {
  IdPerson string             `gorm:"primary_key:true"`
  Accounts []CustomizeAccount `gorm:"many2many:PersonAccount;association_foreignkey:idAccount;foreignkey:idPerson"`
}

type CustomizeAccount struct {
  IdAccount string `gorm:"primary_key:true"`
  Name      string
}
```
外键会为两个结构体创建一个多对多的关系，并且这个关系将通过外键customize_person_id_person 和 customize_account_id_account 保存到中间表 PersonAccount。

### 中间表外键
如果你想改变中间表的外键，你可以用标签 association_jointable_foreignkey, jointable_foreignkey
```go
type CustomizePerson struct {
  IdPerson string             `gorm:"primary_key:true"`
  Accounts []CustomizeAccount `gorm:"many2many:PersonAccount;foreignkey:idPerson;association_foreignkey:idAccount;association_jointable_foreignkey:account_id;jointable_foreignkey:person_id;"`
}

type CustomizeAccount struct {
  IdAccount string `gorm:"primary_key:true"`
  Name      string
}
```
### 自引用
为了定义一个自引用的多对多关系，你不得不改变中间表的关联外键。

和来源表外键不同的是它是通过结构体的名字和主键生成的，例如：
```go
type User struct {
  gorm.Model
  Friends []*User `gorm:"many2many:friendships;association_jointable_foreignkey:friend_id"`
}
```
GORM 将创建一个带外键 user_id 和 friend_id 的中间表， 并且使用它去保存用户表的自引用关系。

然后你可以像普通关系一样操作它， 例如：
```go
DB.Preload("Friends").First(&user, "id = ?", 1)

DB.Model(&user).Association("Friends").Append(&User{Name: "friend1"}, &User{Name: "friend2"})

DB.Model(&user).Association("Friends").Delete(&User{Name: "friend2"})

DB.Model(&user).Association("Friends").Replace(&User{Name: "new friend"})

DB.Model(&user).Association("Friends").Clear()

DB.Model(&user).Association("Friends").Count()
```
### 使用多对多
```go
db.Model(&user).Related(&languages, "Languages")
//// SELECT * FROM "languages" INNER JOIN "user_languages" ON "user_languages"."language_id" = "languages"."id" WHERE "user_languages"."user_id" = 111

//  当查询用户时预加载 Language
db.Preload("Languages").First(&user)
```
## 关联
### 自动创建/更新
GORM 将在创建或保存一条记录的时候自动保存关联和它的引用，如果关联有一个主键， GORM 将调用 Update 来更新它， 不然，它将会被创建。
```go
user := User{
    Name:            "jinzhu",
    BillingAddress:  Address{Address1: "Billing Address - Address 1"},
    ShippingAddress: Address{Address1: "Shipping Address - Address 1"},
    Emails:          []Email{
        {Email: "jinzhu@example.com"},
        {Email: "jinzhu-2@example@example.com"},
    },
    Languages:       []Language{
        {Name: "ZH"},
        {Name: "EN"},
    },
}

db.Create(&user)
//// BEGIN TRANSACTION;
//// INSERT INTO "addresses" (address1) VALUES ("Billing Address - Address 1");
//// INSERT INTO "addresses" (address1) VALUES ("Shipping Address - Address 1");
//// INSERT INTO "users" (name,billing_address_id,shipping_address_id) VALUES ("jinzhu", 1, 2);
//// INSERT INTO "emails" (user_id,email) VALUES (111, "jinzhu@example.com");
//// INSERT INTO "emails" (user_id,email) VALUES (111, "jinzhu-2@example.com");
//// INSERT INTO "languages" ("name") VALUES ('ZH');
//// INSERT INTO user_languages ("user_id","language_id") VALUES (111, 1);
//// INSERT INTO "languages" ("name") VALUES ('EN');
//// INSERT INTO user_languages ("user_id","language_id") VALUES (111, 2);
//// COMMIT;

db.Save(&user)
```
### 关闭自动更新
如果你的关联记录已经存在在数据库中， 你可能会不想去更新它。

你可以设置 gorm:association_autoupdate 为 false
```go
// 不更新有主键的关联，但会更新引用
db.Set("gorm:association_autoupdate", false).Create(&user)
db.Set("gorm:association_autoupdate", false).Save(&user)
或者使用 GORM 的标签， gorm:"association_autoupdate:false"

type User struct {
  gorm.Model
  Name       string
  CompanyID  uint
  // 不更新有主键的关联，但会更新引用
  Company    Company `gorm:"association_autoupdate:false"`
}
```
### 关闭自动创建
即使你禁用了 AutoUpdating, 仍然会创建没有主键的关联，并保存它的引用。

你可以通过把 gorm:association_autocreate 设置为 false 来禁用这个行为。
```go
// 不创建没有主键的关联，不保存它的引用。
db.Set("gorm:association_autocreate", false).Create(&user)
db.Set("gorm:association_autocreate", false).Save(&user)
或者使用 GORM 标签， gorm:"association_autocreate:false"

type User struct {
  gorm.Model
  Name       string
  // 不创建没有主键的关联，不保存它的引用。
  Company1   Company `gorm:"association_autocreate:false"`
}
```
### 关闭自动创建/更新
禁用 AutoCreate 和 AutoUpdate，你可以一起使用它们两个的设置。
```go
db.Set("gorm:association_autoupdate", false).Set("gorm:association_autocreate", false).Create(&user)

type User struct {
  gorm.Model
  Name    string
  Company Company `gorm:"association_autoupdate:false;association_autocreate:false"`
}
```
或者使用 gorm:save_associations
```go
db.Set("gorm:save_associations", false).Create(&user)
db.Set("gorm:save_associations", false).Save(&user)

type User struct {
  gorm.Model
  Name    string
  Company Company `gorm:"association_autoupdate:false"`
}
```
### 关闭保存引用
如果你不想当更新或保存数据的时候保存关联的引用， 你可以使用下面的技巧
```go
db.Set("gorm:association_save_reference", false).Save(&user)
db.Set("gorm:association_save_reference", false).Create(&user)
或者使用标签

type User struct {
  gorm.Model
  Name       string
  CompanyID  uint
  Company    Company `gorm:"association_save_reference:false"`
}
```
### 关联模式
关联模式包含一些可以轻松处理与关系相关的事情的辅助方法。
```go
// 开启关联模式
var user User
db.Model(&user).Association("Languages")
// `user` 是源表，必须包含主键
// `Languages` 是源表关系字段名称。
// 只有上面两个条件都能匹配，关联模式才会生效， 检查是否正常：
// db.Model(&user).Association("Languages").Error
```
### 查找关联
查找匹配的关联
```go
db.Model(&user).Association("Languages").Find(&languages)
```
### 增加关联
为 many to many， has many 新增关联， 为 has one, belongs to 替换当前关联
```go
db.Model(&user).Association("Languages").Append([]Language{languageZH, languageEN})
db.Model(&user).Association("Languages").Append(Language{Name: "DE"})
```
### 替换关联
用一个新的关联替换当前关联
```go
db.Model(&user).Association("Languages").Replace([]Language{languageZH, languageEN})
db.Model(&user).Association("Languages").Replace(Language{Name: "DE"}, languageEN)
```
### 删除关联
删除源和参数对象之间的关系， 只会删除引用，不会删除他们在数据库中的对象。
```go
db.Model(&user).Association("Languages").Delete([]Language{languageZH, languageEN})
db.Model(&user).Association("Languages").Delete(languageZH, languageEN)
```
### 清理关联
删除源和当前关联之间的引用，不会删除他们的关联
```go
db.Model(&user).Association("Languages").Clear()
```
统计关联
返回当前关联的统计数
```go
db.Model(&user).Association("Languages").Count()
```
## 预加载
### 预加载
```go
db.Preload("Orders").Find(&users)
//// SELECT * FROM users;
//// SELECT * FROM orders WHERE user_id IN (1,2,3,4);

db.Preload("Orders", "state NOT IN (?)", "cancelled").Find(&users)
//// SELECT * FROM users;
//// SELECT * FROM orders WHERE user_id IN (1,2,3,4) AND state NOT IN ('cancelled');

db.Where("state = ?", "active").Preload("Orders", "state NOT IN (?)", "cancelled").Find(&users)
//// SELECT * FROM users WHERE state = 'active';
//// SELECT * FROM orders WHERE user_id IN (1,2) AND state NOT IN ('cancelled');

db.Preload("Orders").Preload("Profile").Preload("Role").Find(&users)
//// SELECT * FROM users;
//// SELECT * FROM orders WHERE user_id IN (1,2,3,4); // has many
//// SELECT * FROM profiles WHERE user_id IN (1,2,3,4); // has one
//// SELECT * FROM roles WHERE id IN (4,5,6); // belongs to
```
### 自动预加载
始终自动预加载的关联
```go
type User struct {
  gorm.Model
  Name       string
  CompanyID  uint
  Company    Company `gorm:"PRELOAD:false"` //没有预加载
  Role       Role                           // 已经预加载
}

db.Set("gorm:auto_preload", true).Find(&users)
```
### 嵌套预加载
```go
db.Preload("Orders.OrderItems").Find(&users)
db.Preload("Orders", "state = ?", "paid").Preload("Orders.OrderItems").Find(&users)
```
### 自定义预加载 SQL
您可以通过传入func（db * gorm.DB）* gorm.DB来自定义预加载SQL，例如：
```go
db.Preload("Orders", func(db *gorm.DB) *gorm.DB {
    return db.Order("orders.amount DESC")
}).Find(&users)
//// SELECT * FROM users;
//// SELECT * FROM orders WHERE user_id IN (1,2,3,4) order by orders.amount DESC;
```


# gorm gen
## gorm 例子
Gen 支持所有GORM Driver从数据库生成结构, 使用示例:
```go
package main

import "gorm.io/gen"

func main() {
  g := gen.NewGenerator(gen.Config{
    //  设置输出路径
    OutPath: "../query",
    Mode: gen.WithoutContext|gen.WithDefaultQuery|gen.WithQueryInterface, // 选择生成模式
  })
//  建立数据库连接
  gormdb, _ := gorm.Open(mysql.Open("root:@(127.0.0.1:3306)/demo?charset=utf8mb4&parseTime=True&loc=Local"))
  g.UseDB(gormdb) // 选择数据库连接

  // 为结构模型生成基本类型安全的 DAO API。用户的以下约定

  g.ApplyBasic(
  // Generate struct `User` based on table `users`
  g.GenerateModel("users"),

  // Generate struct `Employee` based on table `users`
  g.GenerateModelAs("users", "Employee"),


// Generate struct `User` based on table `users` and generating options
  g.GenerateModel("users", gen.FieldIgnore("address"), gen.FieldType("id", "int64")),

  )
g.ApplyBasic(
// 从当前数据库的所有表生成结构
g.GenerateAllTable()...,
)
  // 生成代码
  g.Execute()
}

```


## 模板方法
当从数据库生成结构时，您也可以通过面的方式，给生成的model添加模板方法，例如：
```go
type CommonMethod struct {
    ID   int32
    Name *string
}

func (m *CommonMethod) IsEmpty() bool {
    if m == nil {
        return true
    }
    return m.ID == 0
}

func (m *CommonMethod) GetName() string {
    if m == nil || m.Name == nil {
        return ""
    }
    return *m.Name
}

// 将 IsEmpty 方法添加到生成的“People”结构中
g.GenerateModel("people", gen.WithMethod(CommonMethod{}.IsEmpty))

// 将CommonMethod上定义的所有方法添加到生成的“User”结构中
g.GenerateModel("user", gen.WithMethod(CommonMethod))
```

生成的代码如下所示：
```go
type Person struct {
  // ...
}

func (m *Person) IsEmpty() bool {
  if m == nil {
    return true
  }
  return m.ID == 0
}


// Generated User struct
type User struct {
  // ...
}

func (m *User) IsEmpty() bool {
  if m == nil {
    return true
  }
  return m.ID == 0
}

func (m *User) GetName() string {
  if m == nil || m.Name == nil {
    return ""
  }
  return *m.Name
}

```

## 自定义表名称
当从数据库生成结构时，您也可以通过实现自己的TableName方法，例如：
```go

type CommonMethod struct {
    ID   int32
    Name *string
}

// TableName 
func (m CommonMethod) TableName() string {
    return "@@table"
}

// TableName table name with gorm NamingStrategy
func (m CommonMethod) TableName(namer schema.Namer) string {
    if namer == nil {
        return "@@table"
    }
    return namer.TableName("@@table")
}

// 生成的“user”结构的表名方法
g.GenerateModel("user", gen.WithMethod(CommonMethod{}.TableName))

// 自定义生成的所有结构的表名方法
g.WithOpts(gen.WithMethod(CommonMethod{}.TableName))

// 为生成的所有结构设置默认 DIY 表名方法
g.WithOpts(gen.WithMethod(gen.DefaultMethodTableWithNamer))
```


## Field Options
以下是可以在生成模型/生成模型期间使用的选项

FieldNew           // 创建一个新字段
FieldIgnore        // 忽略一个字段
FieldIgnoreReg     // 正则匹配的方法忽略字段
FieldRename        // 重命名结构体的字段
FieldComment       // 在生成的结构中指定字段注释
FieldType          // 指定字段类型
FieldTypeReg       // specify field type (match with regexp)
FieldGenType       // 指定字段生成类型
FieldGenTypeReg    // specify field gen type (match with regexp)
FieldTag           // 指定 gorm 和 JSON 标记
FieldJSONTag       // specify json tag
FieldJSONTagWithNS // 使用名称策略指定 JSON 标记
FieldGORMTag       // specify gorm tag
FieldNewTag        // 追加一个新字段
FieldNewTagWithNS  // 使用名称策略指定新标记
FieldTrimPrefix    // 修剪列前缀
FieldTrimSuffix    // 修剪列后缀
FieldAddPrefix     // 将前缀添加到结构字段的名称
FieldAddSuffix     // 将后缀添加到结构字段的名称
FieldRelate        // 指定与其他表的关系
FieldRelateModel   // 确定与现有模型的关系
## 全局生成选项
Gen 有一些全局选项可以在 gen.Config中设置：
```go

g := gen.NewGenerator(gen.Config{
  // 如果希望可为空字段生成属性为指针类型，请将 FieldNullable 设置为 true
  FieldNullable: true,
  // 如果要分配在“创建”API 中具有默认值的字段，请将 FieldCoverable 设置为 true
  FieldCoverable: true,
  // 如果要生成具有无符号整数类型的字段，请将字段可签名设置为 true
  FieldSignable: true,
  // 如果要从数据库生成索引标记，请将 FieldWithIndexTag 设置为 true
  FieldWithIndexTag: true,
  // 如果要从数据库生成类型标记，请将 FieldWithTypeTag 设置为 true
  FieldWithTypeTag: true,
  // if you need unit tests for query code, set WithUnitTest true
  WithUnitTest: true,
})
```
```go
//  设置获取数据库名称函数
WithDbNameOpts(opts ...model.SchemaNameOpt)

//  指定表名命名策略，仅在从数据库同步表时有效
WithTableNameStrategy(ns func(tableName string) (targetTableName string))

// 指定模型结构名称命名策略，仅在从数据库同步表时有效
// 如果返回空字符串，则将忽略该表
WithModelNameStrategy(ns func(tableName string) (modelName string))

// 指定文件名命名策略，仅在从数据库同步表时有效
WithFileNameStrategy(ns func(tableName string) (fileName string))

// 指定 JSON 标记命名策略
WithJSONTagNameStrategy(ns func(columnName string) (tagContent string))

// 指定数据类型映射关系，仅在从 DB 同步表时工作
WithDataTypeMap(newMap map[string]func(gorm.ColumnType) (dataType string))

// 指定导入包路径
WithImportPkgPath(paths ...string)

// 指定全局模型选项
WithOpts(opts ...ModelOpt)

```

## 数据类型映射
指定model属性类型和 db 字段类型之间的映射关系。
```go

var dataMap = map[string]func(gorm.ColumnType) (dataType string){
    // int mapping
    "int": func(columnType gorm.ColumnType) (dataType string) {
        if n, ok := columnType.Nullable(); ok && n {
            return "*int32"
        }
        return "int32"
    },

    // bool mapping
    "tinyint": func(columnType gorm.ColumnType) (dataType string) {
        ct, _ := columnType.ColumnType()
        if strings.HasPrefix(ct, "tinyint(1)") {
            return "bool"
        }
        return "byte"
    },
}

g.WithDataTypeMap(dataMap)

```
## Gen Tool
Gen Tool 是一个没有依赖关系的二进制文件，可以用来从数据库生成结构

### Install
```go
go install gorm.io/gen/tools/gentool@latest
```

### Usage
gentool -h
```cmd

Usage of gentool:
 -c string
      配置文件路径
 -db string
       选择数据库种类
 -dsn string
       设置数据库连接地址
 -fieldNullable
       当字段可为空时，使用指针生成
 -fieldWithIndexTag
       使用 GORM 索引标签生成字段
 -fieldWithTypeTag
       生成带有 GORM 列类型标记的字段
 -modelPkgName string
       生成的模型代码的包名称
 -outFile string
       查询代码文件名，默认：gen.go
 -outPath string
      指定输出目录
 -tables string
       输入所需的数据表或将其留空
 -onlyModel
       仅生成模型
 -withUnitTest
       为查询代码生成单元测试
 -fieldSignable
       检测整数字段的无符号类型，调整生成的数据类型
```

**c**
配置文件名、默认值 “”、命令行选项的优先级高于配置文件。

**db**
指定Driver，默认值“mysql”

**dsn**
用于连接数据库的DSN 例子："root:password@tcp(localhost:3306)/test?charset=utf8mb4&parseTime=True"

**fieldNullable**
当字段允许空时用指针生成

**fieldWithIndexTag**
生成带有gorm index 标签的字段

**fieldWithTypeTag**
生成带有gorm type标签的字段

**modelPkgName**
生成模型代码包名称。

**outFile**
Genrated 查询代码文件名称，默认值：gen.go

**outPath**
指定输出目录(默认 “./dao/query”)

**tables**
指定要生成的表名称，默认所有表。

eg :
```p
--tables="orders"       # generate from `orders`

--tables="orders,users" # generate from `orders` and `users`

--tables=""             # generate from all tables
```
Generate some tables code.

withUnitTest
生成单元测试，默认值 false, 选项: false / true

fieldSignable
Use signable datatype as field type, default value false, options: false / true

### Example
gentool -dsn "user:pwd@tcp(localhost:3306)/database?charset=utf8mb4&parseTime=True&loc=Local" -tables "orders,doctor"
gentool -c "./gen.tool"
```yaml
version: "0.1"
database:
  # consult[https://gorm.io/docs/connecting_to_the_database.html]"
  dsn : "username:password@tcp(address:port)/db?charset=utf8mb4&parseTime=true&loc=Local"
  # input mysql or postgres or sqlite or sqlserver. consult[https://gorm.io/docs/connecting_to_the_database.html]
  db  : "mysql"
  # enter the required data table or leave it blank.You can input : orders,users,goods
  tables  : "user"
  # specify a directory for output
  outPath :  "./dao/query"
  # query code file name, default: gen.go
  outFile :  ""
  # generate unit test for query code
  withUnitTest  : false
  # generated model code's package name
  modelPkgName  : ""
  # generate with pointer when field is nullable
  fieldNullable : false
  # generate field with gorm index tag
  fieldWithIndexTag : false
  # generate field with gorm column type tag
  fieldWithTypeTag  : false
```