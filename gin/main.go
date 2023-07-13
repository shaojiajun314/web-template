package main

import (
	_ "web/db"
	_ "web/etc"
	"web/http_server"
	_ "web/db/models"
)

func main() {
	httpserver.Run()
}
