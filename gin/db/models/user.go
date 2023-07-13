package models

import (
  "time"

  // "encoding/json"
)


type BaseModel struct {
    ID        uint64      `gorm:"primarykey;type:bigint auto_increment"`
    CreatedAt time.Time   `gorm:"autoCreateTime"`
    UpdatedAt time.Time   `gorm:"autoUpdateTime"`
}


type User struct {
    BaseModel
    ID              uint64      `gorm:"primarykey;type:bigint auto_increment"`
    Address         string
}