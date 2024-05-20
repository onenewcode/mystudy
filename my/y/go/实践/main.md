# 日期转换
## 问题描述
由于通过hertz中，进行web开发，需要进行日期绑定，但是由于前端传过来的是json，且日期格式为yyyy-MM-dd HH:mm:ss 类型但是go通过json包进行自定义结构体进行转换时，并不能进行日期转换格式的指定。所以相比java，来说进行日期进行转换比较繁琐。、
## 解决方法
### 自定义结构体Datetime+自定义临时结构体
```go
// 设置日期格式解析
type DateTime time.Time

func (t DateTime) MarshalJSON() ([]byte, error) {
	var stamp = fmt.Sprintf("\"%s\"", time.Time(t).Format("2006-01-02 15:04:05"))
	return []byte(stamp), nil
}
func (t *DateTime) UnmarshalJSON(b []byte) error {
	str := string(b)
	parse, err := time.Parse("2006-01-02 15:04:05", strings.Trim(str, "\""))
	if err != nil {
		return err
	}
	t = (*DateTime)(&parse)
	return err
}

type OrderDTO struct {
	BeginTime time.Time `json:"begin_time"`
	EndTime   time.Time `json:"end_time"`
	UserId    int64     `json:"user_id,omitempty"`
}
type tmpJSON OrderDTO
type tmp struct {
	tmpJSON
	BeginTime DateTime `json:"begin_time"`
	EndTime   DateTime `json:"end_time"`
}

func (o OrderDTO) MarshalJSON() ([]byte, error) {
	p := &tmp{
		tmpJSON:   (tmpJSON)(o),
		BeginTime: DateTime(o.BeginTime),
		EndTime:   DateTime(o.EndTime),
	}
	marshal, err := json.Marshal(p)
	if err != nil {
		return nil, err
	}
	return marshal, err
}

func (o *OrderDTO) UnmarshalJSON(b []byte) error {
	var t tmp
	err := json.Unmarshal(b, &t)
	t.tmpJSON.BeginTime, t.tmpJSON.EndTime = (time.Time)(t.BeginTime), (time.Time)(t.EndTime)
	if err != nil {
		return err
	}
	o = (*OrderDTO)(&t.tmpJSON)
	return nil
}
func main() {
	my := OrderDTO{
		time.Now(),
		time.Now(),
		123,
	}
	str, _ := my.MarshalJSON()
	fmt.Printf("%s", str)
}

```
效果
```shell
{"user_id":123,"begin_time":"2024-05-20 10:09:17","end_time":"2024-05-20 10:09:17"}
```
#### 代码分析
首先我们定义了一个自定义结构体，它是我们日期类的一个别名，但是他决定了我们的日期类是序列化的格式。

接着我们自定义一个临时的结构体，然后通过一个临时结构体来进行结构转换。