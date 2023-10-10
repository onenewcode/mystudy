package util

import (
	"github.com/dgrijalva/jwt-go"
	"go_demo/pkg/setting"
	"time"
)

// go中string与[]byte的互换
// secret秘密
var jwtSecret = []byte(setting.AppSetting.JwtSecret)

type Claims struct {
	Username string `json:"username"`
	Password string `json:"password"`
	//claim索赔
	jwt.StandardClaims
}

// Generate 生成，创造，产生
func GenerateToken(username, password string) (string, error) {
	nowTime := time.Now()
	//expire 到期，过期
	expireTime := nowTime.Add(3 * time.Hour)

	claims := Claims{
		username,
		password,
		jwt.StandardClaims{
			//expire到期，过期
			//转化成int格式
			ExpiresAt: expireTime.Unix(),
			//Issuer 发行
			Issuer: "gin-blog",
		},
	}

	tokenClaims := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	//Signed 签署
	token, err := tokenClaims.SignedString(jwtSecret)

	return token, err
}

// Parse 解析
func ParseToken(token string) (*Claims, error) {
	tokenClaims, err := jwt.ParseWithClaims(token, &Claims{}, func(token *jwt.Token) (interface{}, error) {
		return jwtSecret, nil
	})

	if tokenClaims != nil {
		if claims, ok := tokenClaims.Claims.(*Claims); ok && tokenClaims.Valid {
			return claims, nil
		}
	}

	return nil, err
}
