package controllers

import (
	"github.com/astaxie/beego"
)

type LivePostingController struct {
	beego.Controller
}

func (c *LivePostingController) Get() {
	c.TplName = "dashboard/auto.html"
	c.Render()
}
