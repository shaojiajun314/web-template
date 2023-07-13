package user

import ()


type UserForm struct {
  Address     string    `json:"address" binding:"required"`
  Sign        string    `json:"sign" binding:"required"`
  TimeStamp   int64     `json:"time_stamp" binding:"required"`
}
