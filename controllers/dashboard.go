package controllers

import (
	"github.com/astaxie/beego"
)

type DashboardController struct {
	beego.Controller
}

func (c *DashboardController) Get() {
	c.TplName = "dashboard/index.html"
	c.Render()
}
