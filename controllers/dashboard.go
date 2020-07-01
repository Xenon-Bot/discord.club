package controllers

import (
	"github.com/Xenon-Bot/discord.club/discord"
	"github.com/astaxie/beego"
)

type DashboardController struct {
	beego.Controller
}

func (c *DashboardController) Get() {
	user, ok := c.GetSession("user").(discord.OauthUser)
	if !ok {
		c.Redirect("/oauth/login", 302)
		return
	}
	c.Data["User"] = &user
	c.TplName = "dashboard/index.html"
	c.Render()
}
