package user

import (
	"github.com/gin-gonic/gin"
)



func RegisterRouter(Router *gin.RouterGroup)  {
	Router.POST("/login", LoginView)
	// Router.POST("/register", view.Register)
}
