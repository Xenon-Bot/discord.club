package services

import (
	"github.com/astaxie/beego/context"
)

type ServiceUpdate struct {
	Service    string
	Identifier string
	Data       interface{}
}

type WebhookRoute struct {
	Handler func(ctx *context.Context, result chan ServiceUpdate)
}

type Service interface {
	Name() string
	Poll(result chan ServiceUpdate)
	WebhookRoute() *WebhookRoute
}
