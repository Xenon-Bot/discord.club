from sanic import Sanic
from motor.motor_asyncio import AsyncIOMotorClient
import aiohttp
import aioredis
from sanic_cors import CORS

import routes
import auth


async def always_json_middleware(_, response):
    if len(response.body) == 0:
        response.body = b"{}"
        response.headers["Content-Type"] = "application/json"


class App(Sanic, auth.AuthMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.blueprint(routes.bp)

        self.mongo = None
        self.db = None
        self.redis = None

        self.session = None

        self.register_listener(self.setup, "before_server_start")
        self.register_listener(self.teardown, "after_server_stop")
        self.register_middleware(always_json_middleware, "response")

        CORS(self)

    async def setup(self, _, loop):
        self.mongo = AsyncIOMotorClient()
        self.db = self.mongo.dclub

        self.session = aiohttp.ClientSession(loop=loop)
        self.redis = await aioredis.create_redis_pool("redis://localhost", loop=loop)

        await routes.setup(self)

    async def teardown(self, _, loop):
        await self.session.close()
        self.redis.close()
        await self.redis.wait_closed()


app = App(name="xenon.bot", load_env="APP_", strict_slashes=False)

app.config.PROXIES_COUNT = 2

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, access_log=True, debug=True, auto_reload=False)
