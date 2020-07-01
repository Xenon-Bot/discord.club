package services

import (
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/context"
)

type ServiceManager struct {
	Services []Service
	Updates  chan ServiceUpdate
}

func (m *ServiceManager) Init() {
	m.Services = make([]Service, 0)
	m.Updates = make(chan ServiceUpdate, 100)
}

func (m *ServiceManager) RegisterService(service Service) {
	m.Services = append(m.Services, service)
	webhookRoute := service.WebhookRoute()
	if webhookRoute != nil {
		beego.Any("/webhooks/"+service.Name(), func(ctx *context.Context) {
			webhookRoute.Handler(ctx, m.Updates)
		})
	}
}

func (m *ServiceManager) PollAll() {
	for _, service := range m.Services {
		service.Poll(m.Updates)
	}
}
