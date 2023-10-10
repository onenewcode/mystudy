package jwt

import (
	"go_demo/pkg/e"
	"go_demo/pkg/util"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

// 表单验证
func JWT() gin.HandlerFunc {
	return func(c *gin.Context) {
		var code int
		var data interface{}

		code = e.SUCCESS
		token := c.Query("token")
		if token == "" {

			code = e.INVALID_PARAMS
		} else {
			claims, err := util.ParseToken(token)
			if err != nil {
				code = e.ERROR_AUTH_CHECK_TOKEN_FAIL
			} else if time.Now().Unix() > claims.ExpiresAt {
				code = e.ERROR_AUTH_CHECK_TOKEN_TIMEOUT
			}
		}

		if code != e.SUCCESS {
			c.JSON(http.StatusUnauthorized, gin.H{
				"code": code,
				"msg":  e.GetMsg(code),
				"data": data,
			})
			//Abort 在被调用的函数中阻止挂起函数。注意这将不会停止当前的函数。例如，你有一个验证当前的请求是否是认证过的 Authorization 中间件。
			//如果验证失败(例如，密码不匹配)，调用 Abort 以确保这个请求的其他函数不会被调用。
			c.Abort()
			return
		}

		c.Next()
	}
}
