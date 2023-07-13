package v1

import (
  "net/http"
	"github.com/gin-gonic/gin"

  "web/http_server/v1/user"
  "web/lib/http/middleware"
)


func RegisterRouter(Router *gin.RouterGroup)  {
  Router.GET("/version", func(c *gin.Context) {
    c.String(http.StatusOK, "1.0.0")
  })
  user.RegisterRouter(Router.Group("user"))

  api := Router.Group("")
  api.Use(middleware.AuthMiddleware)
}
