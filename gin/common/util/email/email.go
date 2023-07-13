package email

import (
  "fmt"
  "bytes"
  "html/template"
	"gopkg.in/gomail.v2"
)


const (
	MailPort = 25
  MailHost = "smtp.163.com"
  MailUser = "yellowBear0513@163.com"
  MailPwd = "DBXZTKTDOCJYJNOD"
  Nickname = "shaw"
)

var D *gomail.Dialer


func NewSender()  {
	D = gomail.NewDialer(MailHost, MailPort, MailUser, MailPwd)
}


func Send(
  to string,
  subject string,
  contentType string,
  body string,
) {
  if D == nil {
    NewSender()
  }
  m := gomail.NewMessage()
  m.SetHeader("From", Nickname + "<" +MailUser+ ">")
	m.SetHeader("To", to)
	m.SetHeader("Subject", subject)
  if contentType == "" {
    contentType = "text/html"
  }
  fmt.Println(body, "bbbbb")
	m.SetBody(contentType, body)
  e := D.DialAndSend(m)
  fmt.Println(e, "eeeee")
}


func SendTemplate(
  to string,
  subject string,
  templ string,
  kv map[string]string,
) {
  tpl, _ := template.ParseFiles(templ)
  b := new(bytes.Buffer)
  tpl.Execute(b, kv)
  Send(
    to,
    subject,
    "text/html",
    string(b.String()),
  )
}
