package routers

import (
	"github.com/Xenon-Bot/discord.club/controllers"

	"github.com/astaxie/beego"
	"github.com/astaxie/beego/context"
)

func init() {
	dashboardNS := beego.NewNamespace("/db",
		beego.NSAny("", func(ctx *context.Context) {
			ctx.Redirect(302, "/db/embedg")
		}),
		beego.NSRouter("/embedg", &controllers.EmbedGController{}),
		beego.NSRouter("/live", &controllers.LivePostingController{}),
	)
	beego.AddNamespace(dashboardNS)
}
