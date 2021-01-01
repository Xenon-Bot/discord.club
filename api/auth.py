import jwt
import typing
from sanic import response
from datetime import datetime, timedelta
import traceback


def requires_token(handler):
    async def wrapper(request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if token is None:
            return response.json({"error": "Unauthorized"}, status=401)

        try:
            data = request.app.decode_token(token)
        except jwt.DecodeError:
            traceback.print_exc()
            return response.json({"error": "Invalid token"}, status=401)

        return await handler(request, data["uid"], *args, **kwargs)

    return wrapper


class AuthMixin:
    session: typing.Any
    db = typing.Any
    config: typing.Any

    async def exchange_token(self, code):
        async with self.session.post(
                url="https://discord.com/api/v8/oauth2/token",
                data={
                    "code": code,
                    "client_id": self.config.CLIENT_ID,
                    "client_secret": self.config.CLIENT_SECRET,
                    "redirect_uri": self.config.REDIRECT_URI,
                    "grant_type": "authorization_code",
                    "scope": "identify"
                },
        ) as resp:
            resp.raise_for_status()
            token_data = await resp.json()
            expires_at = datetime.utcnow() + timedelta(seconds=token_data.pop("expires_in"))
            token_data["expires_at"] = expires_at.timestamp()

        async with self.oauth_request("GET", "/users/@me", token=token_data["access_token"]) as resp:
            resp.raise_for_status()
            user_data = await resp.json()

        await self.db.sessions.update_one(
            {"_id": user_data["id"]},
            {"$set": {"tokens": token_data, "user": user_data}},
            upsert=True
        )

        return self.encode_token({"uid": user_data["id"]})

    def oauth_request(self, method, path, token, **kwargs):
        url = f"https://discord.com/api/v8{path}"
        return self.session.request(method, url, **kwargs, headers={"Authorization": f"Bearer {token}"})

    def encode_token(self, data):
        return jwt.encode(data, str(self.config.JWT_SECRET))

    def decode_token(self, token):
        return jwt.decode(token, str(self.config.JWT_SECRET))
