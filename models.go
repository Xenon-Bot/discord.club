package main

import (
	"github.com/astaxie/beego/orm"
)

type Embed struct {
	Id   int
	Name string
}

func init() {
	orm.RegisterModel(new(Embed))
}
