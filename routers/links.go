package routers

import (
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/context"
)

func init() {
	beego.Get("/discord", func(ctx *context.Context) {
		ctx.Redirect(302, "https://discord.gg/zwWENhu")
	})
}
