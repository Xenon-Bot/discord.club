package util

import (
	"fmt"
	"strconv"

	"github.com/astaxie/beego"
	"github.com/astaxie/beego/httplib"
)

const discordApi = "https://discord.com/api/v6"
const discordCdn = "https://cdn.discordapp.com"

type TokenData struct {
	AccessToken  string `json:"access_token"`
	TokenType    string `json:"token_type"`
	ExpiresIn    int    `json:"expires_in"`
	RefreshToken string `json:"refresh_token"`
	Scope        string `json:"scope"`
}

type OauthUser struct {
	Id            string `json:"id"`
	Username      string `json:"username"`
	Discriminator string `json:"discriminator"`
	Avatar        string `json:"avatar"`
}

func (u *OauthUser) avatarUrl() string {
	if u.Avatar == "" {
		i, err := strconv.Atoi(u.Discriminator)
		if err != nil {
			return ""
		}
		return fmt.Sprint(discordCdn, "/embed/avatars/", i%5, ".png")
	}

	return fmt.Sprint(discordCdn, "/avatars/", u.Id, "/", u.Avatar, ".png")
}

func ExchangeToken(authCode string) (TokenData, error) {
	req := httplib.Post(discordApi + "/oauth2/token")

	req.Param("client_id", beego.AppConfig.String("oauthClientId"))
	req.Param("client_secret", beego.AppConfig.String("oauthClientSecret"))
	req.Param("grant_type", "authorization_code")
	req.Param("code", authCode)
	req.Param("redirect_uri", beego.AppConfig.String("oauthRedirectUri"))
	req.Param("scope", "identify")
	req.Header("Content-Type", "application/x-www-form-urlencoded")

	var resp TokenData
	err := req.ToJSON(&resp)
	return resp, err
}

func GetOauthUser(accessToken string) (OauthUser, error) {
	req := httplib.Get(discordApi + "/users/@me")
	req.Header("Authorization", "Bearer "+accessToken)

	var resp OauthUser
	err := req.ToJSON(&resp)
	return resp, err
}
