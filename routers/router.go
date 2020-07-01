package routers

import (
	"github.com/Xenon-Bot/discord.club/controllers"
	"github.com/Xenon-Bot/discord.club/discord"

	"github.com/astaxie/beego"
	"github.com/astaxie/beego/context"
)

func init() {
	beego.ErrorController(&controllers.ErrorController{})
	beego.Router("/", &controllers.MainController{})

	dashboardNS := beego.NewNamespace("/dashboard",
		// Checks if user is logged in
		beego.NSBefore(func(ctx *context.Context) {
			token, ok := ctx.Input.Session("token").(discord.TokenData)
			if !ok {
				// User is not logged in
				ctx.Redirect(302, "/oauth/login")
				return
			}

			// Expose access token to the frontend
			ctx.Output.Cookie("token", token.AccessToken)
		}),
		beego.NSRouter("/", &controllers.DashboardController{}),
	)
	beego.AddNamespace(dashboardNS)
}
