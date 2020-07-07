package controllers

import (
	"github.com/astaxie/beego"
)

type EmbedGController struct {
	beego.Controller
}

func (c *EmbedGController) Get() {
	c.TplName = "dashboard/embedg.html"
	c.Render()
}
