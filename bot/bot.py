from discord.ext import commands as cmd
import discord
from motor.motor_asyncio import AsyncIOMotorClient
import aioredis
from os import environ as env
import aiohttp
import traceback
import sys


class DiscordClubBot(cmd.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=">",
            intents=discord.Intents(
                messages=True,
                guilds=True
            ),
            shard_count=int(env["SHARD_COUNT"]) if env.get("SHARD_COUNT") else None,
            activity=discord.Activity(
                name=f"discord.club | >help",
                type=discord.ActivityType.watching
            )
        )
        self.redis = None
        self.session = None
        self.db = AsyncIOMotorClient(env.get("MONGO_URL", "mongodb://127.0.0.1"))

        self.api_host = env.get("API_HOST", "http://localhost:8080")
        self.site_host = env.get("SITE_HOST", "http://localhost:3000")

        for module in {"basics", "help"}:
            self.load_extension(f"modules.{module}")

    async def on_command_error(self, ctx, e):
        if isinstance(e, cmd.CheckFailure):
            await ctx.send(str(e))
        else:
            tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            print(tb, file=sys.stderr)
            await ctx.send(f"**Unexpected Error**```py\n{tb}\n```")

    async def on_ready(self):
        print("bot ready")

    async def on_shard_connect(self, shard_id):
        print(f"shard {shard_id} connecting")

    async def on_shard_ready(self, shard_id):
        print(f"shard {shard_id} ready")

    async def start(self, *args, **kwargs):
        self.redis = await aioredis.create_redis_pool(env.get("REDIS_URL", "redis://127.0.0.1"))
        self.session = aiohttp.ClientSession()

        await super().start(*args, **kwargs)


if __name__ == "__main__":
    bot = DiscordClubBot()
    bot.run(env.get("TOKEN"))
