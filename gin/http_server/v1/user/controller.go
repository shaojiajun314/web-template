package user

import (
  "fmt"
  "time"
  "strconv"
  "strings"
  "github.com/sirupsen/logrus"

  "web/db"
  "web/etc"
  "web/db/models"
  "web/common/error"
  "web/common/util/eth"
  "web/lib/http/jwt"
)



func LoginController(f UserForm) (string, *error.Error) {
  address, _ := f.Address, f.Sign
  // warnning debug
  if !etc.DEBUG {
    timeUnix := time.Now().Unix()
    dur := timeUnix - f.TimeStamp
    if dur > etc.USERSIGNEXPIRED || dur < 0 {
      return "", &error.Error{
        Code: 1100110,
        Hits: f.Address,
      }
    }
    if !(strings.HasPrefix(f.Address, "0x") && strings.HasPrefix(f.Sign, "0x")) {
      return "", &error.Error{
        Code: 1100120,
        Hits: "address and sign must startwith 0x",
      }
    }
    if ! eth.VerifySig(
      f.Address,
      f.Sign,
      []byte(strconv.Itoa(int(f.TimeStamp))),
    ) {
      return "", &error.Error{
        Code: 1100120,
        Hits: f.Address,
      }
    }
  }

  token, er := jwt.GetJWTToken(address)
  logrus.Infoln("customer user login address: ", f.Address)

  var user models.User

  ret := db.DataBase.Debug().First(&user, models.User{Address: address})
  if ret.RowsAffected == 0 {
    ret = db.DataBase.Debug().Create(&models.User{
      Address: address,
    })
    if ret.RowsAffected == 0 {
      return "", &error.Error{
        Code: 1100110,
        Hits: fmt.Sprintf("create user error: %v", f.Address),
      }
    }
  }
  return token, er
}
