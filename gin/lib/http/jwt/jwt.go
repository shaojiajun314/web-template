package jwt

import (
	"os"
	"fmt"
	"time"
	"errors"
	"github.com/satori/go.uuid"
	"github.com/dgrijalva/jwt-go"

	er "web/common/error"
)


type Claims struct {
	Address 		string 						`json:"address"`
	jwt.StandardClaims
}


var CustomerSigningKey []byte
func init() {
	f, err := os.Open(".sign_key")
  if err != nil {
  		if os.IsNotExist(err) {
  			f, err = os.OpenFile(".sign_key", os.O_WRONLY | os.O_CREATE, 0666)
  			if err != nil {
  				panic(err)
  			}
  			CustomerSigningKey = []byte(uuid.NewV4().String())
  			if n, e := f.Write(CustomerSigningKey);
  				(n != len(CustomerSigningKey) || e != nil) {
  				panic("error")
  			}
  			return
  		} 
      panic(err)
  }
  buf := make([]byte, 128)
  n, e := f.Read(buf)
  if e != nil {
  	panic(e)
  }
  CustomerSigningKey = buf[0:n]
}


func ParseToken(tokenStr string) (*Claims, error) {
	token, err := jwt.ParseWithClaims(
		tokenStr, &Claims{},
		func(token *jwt.Token) (interface{}, error) {
			return CustomerSigningKey, nil
		},
	)
	if err != nil {
		fmt.Println(" token parse err:", err)
		return nil, err
	}
	if claims, ok := token.Claims.(*Claims); ok && token.Valid {
		return claims, nil
	}
	return nil, errors.New("invalid token")
}


func GetJWTToken(address string) (string, *er.Error) {
  claims := Claims{
    address,
    jwt.StandardClaims{
      ExpiresAt: time.Now().Add(7 * time.Hour).Unix(),
      Issuer:    "dogBox",
    },
  }
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	signToken, err := token.SignedString(CustomerSigningKey)
	if err != nil {
		return "", &er.Error{
      Code: 1100010,
      Hits: fmt.Sprintf("%v", err),
    }
  }
  return signToken, nil
}
