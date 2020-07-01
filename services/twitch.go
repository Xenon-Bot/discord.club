package services

import (
	"github.com/astaxie/beego/context"
)

type TwitchData struct {
	Status string
}

type TwitchService struct{}

func (s *TwitchService) Name() string {
	return "twitch"
}

func (s *TwitchService) Poll(result chan ServiceUpdate) {
	// We can't poll twitch manually
}

func (s *TwitchService) WebhookRoute() *WebhookRoute {
	return &WebhookRoute{Handler: s.handleWebhook}
}

func (s *TwitchService) handleWebhook(ctx *context.Context, result chan ServiceUpdate) {
	// TODO handle webhook request by twitch and assemble ServiceUpdate
	result <- ServiceUpdate{Service: "twitch", User: "merlintor", Data: &TwitchData{Status: "live"}}
}
