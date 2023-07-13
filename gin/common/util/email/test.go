package email

import (
  "testing"
)


func TestEmail(t *testing.T) {
  SendTemplate(
    "shaojiajun314@qq.com",
    "subject",
    "./template/hello.html",
    map[string]string{},
  )
}
