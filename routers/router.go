package routers

import (
	"github.com/Xenon-Bot/discord.club/controllers"

	"github.com/astaxie/beego"
)

func init() {
	beego.ErrorController(&controllers.ErrorController{})
	beego.Router("/", &controllers.MainController{})
}
