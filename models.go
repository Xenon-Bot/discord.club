package main

import (
	"github.com/astaxie/beego/orm"
)

type Embed struct {
	Id   int
	Name string
}

type AutoPost struct {
	Id         int
	UserId     string
	Identifier string
	Service    string
}

func init() {
	orm.RegisterModel(new(Embed), new(AutoPost))
}
