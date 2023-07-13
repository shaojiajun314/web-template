package httpserver

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/swaggo/gin-swagger"
	"github.com/swaggo/gin-swagger/swaggerFiles"

	"web/etc"
	_ "web/docs"
	"web/http_server/v1"
	// "web/http_server/http/middleware"
)

func Run() {
	ginApp := gin.Default()

	ginApp.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	api := ginApp.Group("api/v1")
	// api.Use(middleware.AuthMiddleware)
	v1.RegisterRouter(api)

	ginApp.Run(fmt.Sprintf("%v:%d", etc.Host, etc.Port))
}
