package jwt

import (
	"fmt"
	"time"
	"errors"
	"github.com/satori/go.uuid"
	"github.com/dgrijalva/jwt-go"

	er "web/common/error"
)


type ManagerClaims struct {
	UserName 	string 		`json:"username"`
  ID 	      uint 		  `json:"id"`
	jwt.StandardClaims
}


var ManagerSigningKey []byte = []byte(uuid.NewV4().String())


func ParseManagerToken(tokenStr string) (*ManagerClaims, error) {
	token, err := jwt.ParseWithClaims(
		tokenStr, &ManagerClaims{},
		func(token *jwt.Token) (interface{}, error) {
			return ManagerSigningKey, nil
		},
	)
	if err != nil {
		fmt.Println(" token parse err:", err)
		return nil, err
	}
	if claims, ok := token.Claims.(*ManagerClaims); ok && token.Valid {
		return claims, nil
	}
	return nil, errors.New("invalid token")
}


func GetManagerJWTToken(username string, id uint) (string, *er.Error) {
  claims := ManagerClaims{
    username,
    id,
    jwt.StandardClaims{
      ExpiresAt: time.Now().Add(7 * time.Hour).Unix(),
      Issuer:    "LanDao",
    },
  }
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	signToken, err := token.SignedString(ManagerSigningKey)
	if err != nil {
		return "", &er.Error{
      Code: 1100010,
      Hits: fmt.Sprintf("%v", err),
    }
  }
  return signToken, nil
}
