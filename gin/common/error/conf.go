package error


var Conf = map[int]string {
  0: "success",

  1000000: "api error",
  1100000: "user api error",
  1100010: "user api error (jwt)",
  1100020: "username or password is invalidate",
  1100040: "username is already exsited",
  1100110: "sign is expired",
  1100120: "sign is invalid",


  1200000: "media api error",
  1200010: "media api upload file error",

  1300000: "deposit api error",
  1300010: "deposit extra info api error",


  2000000: "transaction error",
  201000: "transaction deposit error",
  201010: "transaction deposit.st or deposit.et error",


  3000000: "manager api error",
  3100010: "manager create tag error",
}
