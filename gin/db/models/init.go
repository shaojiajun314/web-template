package models
import (
	"web/db"
)

func init()  {
	db.DataBase.AutoMigrate(
		&User{},
	)
}
