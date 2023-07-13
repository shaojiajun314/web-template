package db

import (
  "log"
  "fmt"
  "gorm.io/gorm"
  "gorm.io/driver/mysql"

  "web/etc"
)

var DataBase *gorm.DB

func init()  {
  db, er := gorm.Open(
    mysql.Open(
      fmt.Sprintf(
        "%s:%s@tcp(%s:%d)/%s?charset=utf8&parseTime=True&loc=Local&timeout=%s",
        etc.MysqlUName,
        etc.MysqlPWD,
        etc.MysqlHost,
        etc.MysqlPort,
        etc.MysqlDB,
        "10s",
      ),
    ),
    &gorm.Config{
      DisableForeignKeyConstraintWhenMigrating: true,
    },
  )
  if er != nil {
    log.Fatalln("error db connect")
  }

  DataBase = db
  
}
