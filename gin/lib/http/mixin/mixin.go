package mixin

import (
  "fmt"
  "gorm.io/gorm"
  "github.com/gin-gonic/gin"

  "web/common/error"
  "web/lib/http/response"
)


func List(context *gin.Context, qs *gorm.DB)(
    *gorm.DB, int64, int, int,
) {
  var pagination PageNumberPagination
  var total int64
  qs.Session(&gorm.Session{}).Count(&total)
  context.ShouldBindQuery(&pagination)
  size := pagination.Size
  if size <= 0 {
    size = DefaultSize
  }else if size > MaxSize {
    size = MaxSize
  }
  page := pagination.Page
  if page <= 0 {
    page = 1
  }
  qs = qs.Offset((page - 1) * size).Limit(size)
  return qs, total, page, size

}


func ListResponse(
    context *gin.Context,
    data interface{},
    total int64,
    page int,
    size int,
    fields ...string,
) {
  if len(fields) == 0 {
    response.R(
      context,
      0,
      "success",
      map[string]interface{}{
        "count": total,
        "list": data,
        "page": page,
        "size": size,
      },
    )
    return
  }
  responseDatas := ParseSlice(data, fields...)
  response.R(
    context,
    0,
    "success",
    map[string]interface{}{
      "count": total,
      "list": responseDatas,
      "page": page,
      "size": size,
    },
  )
  return
}


func Retrieve(
  context *gin.Context,
  qs *gorm.DB,
  fields ...string,
) (
    bool,
) {
  recieved := make(map[string]interface{})
  ret := qs.First(recieved)
  fmt.Println(recieved)
  if ret.RowsAffected != 1 {
    response.R(
      context,
      100,
      fmt.Sprintf("not found"),
      fmt.Sprintf("not found"),
    )
    return false
  }
  RetrieveResponse(context, recieved, fields...)
  return true
}


func RetrieveResponse(
    context *gin.Context,
    data interface{},
    fields ...string,
) {
  if len(fields) == 0 {
    response.R(
      context,
      0,
      "success",
      data,
    )
    return
  }
  responseDatas := ParseStruct(data, fields...)
  response.R(
    context,
    0,
    "success",
    responseDatas,
  )
  return
}


func CheckJSON(context *gin.Context, form any) bool {
  if e := context.ShouldBindJSON(form); e != nil {
    response.R(
      context,
      100,
      fmt.Sprintf("%v", e),
      fmt.Sprintf("%v", e),
    )
    return false
  }
  return true
}

func CheckQuery(context *gin.Context, form any) bool {
  if e := context.ShouldBindQuery(form); e != nil {
    response.R(
      context,
      100,
      fmt.Sprintf("%v", e),
      fmt.Sprintf("%v", e),
    )
    return false
  }
  return true
}

func CheckUri(context *gin.Context, form any) bool {
  if e := context.ShouldBindUri(form); e != nil {
    response.R(
      context,
      100,
      fmt.Sprintf("%v", e),
      fmt.Sprintf("%v", e),
    )
    return false
  }
  return true
}


func CommonResponse(context *gin.Context, res interface{}, er *error.Error) {
  if er != nil {
    response.R(
      context,
      er.Code,
      er.Message(),
      er.Message(),
    )
    return
  }
  response.R(
    context,
    0,
    "success",
    res,
  )
}
