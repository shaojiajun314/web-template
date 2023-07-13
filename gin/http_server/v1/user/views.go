package user

import (
	"github.com/gin-gonic/gin"

	"web/common/error"
	"web/lib/http/mixin"
)


// @Tags user
// @Summary  customer login
// @Description customer login
// @Accept  json
// @Param UserForm body UserForm true "login form"
// @Success 200 {object} response.Ret	"success"
// @Router /api/v1/user/login [POST]
func LoginView(context *gin.Context) {
	defer func() {
    if r := recover(); r != nil {
			mixin.CommonResponse(context, "", &error.Error{
	      Code: 1100120,
	      Hits: "签名错误",
	    })
    }
  }()
  var f UserForm
	if ok := mixin.CheckJSON(context, &f); !ok {
		return
	}
	token, er := LoginController(f)
	context.SetCookie("Authorization", token, 0, "", "", false, true)
	mixin.CommonResponse(context, token, er)
}
