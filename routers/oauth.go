package routers

import (
	"github.com/Xenon-Bot/discord.club/discord"

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

			tokenData, err := discord.ExchangeToken(authCode)
			if err != nil || tokenData.AccessToken == "" {
				ctx.Abort(400, "Token exchange failed")
				return
			}
			ctx.Output.Session("token", tokenData)

			user, err := discord.GetOauthUser(tokenData.AccessToken)
			if err != nil || user.Id == "" {
				ctx.Abort(400, "Fetching the oauth user failed")
				return
			}
			ctx.Output.Session("user", user)

			ctx.Redirect(302, "/db")
		}),

		beego.NSGet("/logout", func(ctx *context.Context) {
			ctx.Input.CruSession.Delete("token")
			ctx.Input.CruSession.Delete("user")
			ctx.Redirect(302, "/")
		}),
	)
	beego.AddNamespace(oauthNS)

	// Expose the logged in User to the template
	beego.InsertFilter("/*", beego.BeforeExec, func(ctx *context.Context) {
		user, ok := ctx.Input.Session("user").(discord.OauthUser)
		if ok {
			ctx.Input.SetData("User", &user)
		}
	})

	// Check if user is logged for dashboard
	beego.InsertFilter("/db/*", beego.BeforeExec, func(ctx *context.Context) {
		token, ok := ctx.Input.Session("token").(discord.TokenData)
		if !ok {
			// User is not logged in
			ctx.Redirect(302, "/oauth/login")
			return
		}

		// Expose access token to the frontend
		ctx.Output.Cookie("token", token.AccessToken)
	})
}
