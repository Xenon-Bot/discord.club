package routers

import (
	. "discord_club/util"

	"github.com/astaxie/beego"
	"github.com/astaxie/beego/context"
)

func init() {
	oauthNS := beego.NewNamespace("/oauth",
		beego.NSGet("/login", func(ctx *context.Context) {
			ctx.Redirect(302, beego.AppConfig.String("oauthUrl"))
		}),

		beego.NSGet("/callback", func(ctx *context.Context) {
			authCode := ctx.Input.Query("code")
			if authCode == "" {
				ctx.Redirect(302, "/oauth/login")
				return
			}

			tokenData, err := ExchangeToken(authCode)
			if err != nil || tokenData.AccessToken == "" {
				ctx.Abort(400, "Token exchange failed")
				return
			}
			ctx.Output.Session("token", tokenData)

			user, err := GetOauthUser(tokenData.AccessToken)
			if err != nil || user.Id == "" {
				ctx.Abort(400, "Fetching the oauth user failed")
				return
			}
			ctx.Output.Session("user", user)

			ctx.Redirect(302, "/dashboard")
		}),

		beego.NSGet("/logout", func(ctx *context.Context) {
			ctx.Input.CruSession.Delete("token")
			ctx.Input.CruSession.Delete("user")
			ctx.Redirect(302, "/")
		}),
	)
	beego.AddNamespace(oauthNS)
}
