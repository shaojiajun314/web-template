package etc

import (
  "os"
  "log"
  "fmt"
  "flag"
  "strconv"
)


func init() {
    // scheduler server
    host := flag.String("host", Host, "server host")
    port := flag.Int("port", Port, "server port")

    flag.Parse()

    // server
    Host = *host
    Port = *port


    if mysqlUser := os.Getenv("MYSQL_USER"); mysqlUser != "" {
        MysqlUName = mysqlUser
    }
    if mysqlPWD := os.Getenv("MYSQL_PASSWORD"); mysqlPWD != "" {
        MysqlPWD = mysqlPWD
    }
    if mysqlHost := os.Getenv("MYSQL_HOST"); mysqlHost != "" {
        MysqlHost = mysqlHost
    }
    if mysqlPort := os.Getenv("MYSQL_PORT"); mysqlPort != "" {
        if v, e := strconv.Atoi(mysqlPort); e == nil {
            MysqlPort = v
        } else {
            panic(e)
        }
    }
    if mysqlDB := os.Getenv("MYSQL_DATABASE"); mysqlDB != "" {
        MysqlDB = mysqlDB
    }

    DEBUG = os.Getenv("DEBUG") == "true"

    log.Println(fmt.Sprintf(
        `
        // server
        host: %v
        port: %v

        mysql host: %v
        mysql port: %v
        mysql database: %v
        mysql uername: %v
        mysql pssword: %v
        
        debug: %v
        `,
        // server
        Host,
        Port,
        MysqlHost,
        MysqlPort,
        MysqlDB,
        MysqlUName,
        MysqlPWD,
        DEBUG,
    ),)
}