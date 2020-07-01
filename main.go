package main

import (
	"fmt"

	_ "github.com/Xenon-Bot/discord.club/routers"
	"github.com/Xenon-Bot/discord.club/services"
	_ "github.com/astaxie/beego/session/redis"

	"github.com/astaxie/beego"
	"github.com/astaxie/beego/orm"
	_ "github.com/mattn/go-sqlite3"
)

func init() {
	orm.RegisterDriver("sqlite", orm.DRSqlite)
	orm.RegisterDataBase("default", "sqlite3", "data.db")
}

func main() {
	err := orm.RunSyncdb("default", true, false)
	if err != nil {
		fmt.Println(err)
	}

	o := orm.NewOrm()
	o.Using("default")
	orm.Debug = true

	serviceManager := services.ServiceManager{}
	serviceManager.Init()
	serviceManager.RegisterService(&services.TwitchService{})
	go func() {
		for update := range serviceManager.Updates {
			fmt.Println("out")
			fmt.Println(update)
		}
	}()

	beego.Run()
}
