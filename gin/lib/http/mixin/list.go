package mixin

import (
  "strings"
  "reflect"
)

func snakeString(s string) string {
  data := make([]byte, 0, len(s)*2)
  j := false
  num := len(s)
  for i := 0; i < num; i++ {
    d := s[i]
    if i > 0 && d >= 'A' && d <= 'Z' && j {
      data = append(data, '_')
    }
    if d != '_' {
      j = true
    }
    data = append(data, d)
  }
  return strings.ToLower(string(data[:]))
}

func r(key string, ts reflect.Type, vs reflect.Value, rawData interface{}, m *(map[string]interface{})){
  switch vs.Kind() {
  case reflect.Struct:
    for t := 0; t < ts.NumField(); t++ {
      field := ts.Field(t)
      n := field.Name
      if key == n {
        jsonTag := field.Tag.Get("json")
        if jsonTag != "" && jsonTag != "-" {
          key = jsonTag
        }
        (*m)[key] = vs.Field(t).Interface()
        break
      } else if (n == "Model") {
        in := vs.Field(t).Interface()
        r(key, reflect.TypeOf(in), reflect.ValueOf(in), in, m)
      }
    }
  case reflect.Map:
    key = snakeString(key)
    for k, v := range rawData.(map[string]interface{}) {
      if k == key {
        (*m)[key] = v
        break
      }
    }
  }
  
}


func parseStruct(rawData interface{}, fields string) map[string]interface{} {
  fieldsSplited := strings.Split(fields, "|")
  responseData := make(map[string]interface{})
  ts := reflect.TypeOf(rawData)
  vs := reflect.ValueOf(rawData)
  for _, f := range fieldsSplited {
    ss := strings.SplitN(f, ".", 2)
    s := ss[0]
    if len(ss) != 1 {
      for t := 0; t < ts.NumField(); t++ {
        field := ts.Field(t)
        if s == field.Name {
          jsonTag := field.Tag.Get("json")
          if jsonTag != "" && jsonTag != "-" {
            s = jsonTag
          }
          d := vs.Field(t).Interface()
          if reflect.ValueOf(d).Kind() == reflect.Struct {
            responseData[s] = parseStruct(d, ss[1])
          } else {
            responseData[s] = ParseSlice(d, ss[1])
          }
          break
        }
      }
    } else {
      r(s, ts, vs, rawData, &responseData)
      // for t := 0; t < ts.NumField(); t++ {
      //   fmt.Println(ts.Field(t).Name)
      //   n := ts.Field(t).Name
      //   if s == n {
      //     responseData[s] = vs.Field(t).Interface()
      //     break
      //   } else if (n == "Model") {
      //
      //   }
      // }
    }
  }
  return responseData
}


func ParseSlice(rawData interface{}, fields ...string) []map[string]interface{} {
  var responseDatas []map[string]interface{}
  dataSlice := reflect.ValueOf(rawData)

  for i := 0; i < dataSlice.Len(); i++ {
    responseData := parseStruct(dataSlice.Index(i).Interface(), strings.Join(fields, "|"))
    responseDatas = append(responseDatas, responseData)
  }
  return responseDatas
}


func ParseStruct(rawData interface{}, fields ...string) map[string]interface{} {
  return parseStruct(rawData, strings.Join(fields, "|"))
}
