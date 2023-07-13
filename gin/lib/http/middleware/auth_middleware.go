package middleware

import (
  "fmt"
  "github.com/gin-gonic/gin"

  "web/lib/http/jwt"
  "web/lib/http/response"
)


func AuthMiddleware(c *gin.Context) {
  fmt.Println("// TODO: auth middleware start")
  // authHeader := c.Request.Header.Get("Authorization")
  authHeader, err := c.Cookie("Authorization")
  if err != nil {
    authHeader = c.Request.Header.Get("JWT")
    if authHeader == "" {
      response.R(
        c,
        100,
        "invalid cookie",
        "invalid cookie",
      )
      c.Abort()
      return
    }
  }
  d, e := jwt.ParseToken(authHeader)
  c.Set("user", d)
  if e != nil {
    response.R(
      c,
      100,
      fmt.Sprintf("%v", e),
      fmt.Sprintf("%v", e),
    )
    c.Abort()
    return
  }
  fmt.Println("login user %v", d)
  c.Next()
  fmt.Println("// TODO: auth middleware end")
}
