from discord.ext import commands as cmd
import discord
import re
import json
import uuid


class Utilities(cmd.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cmd.command(aliases=("api",))
    async def format(self, ctx, *, text):
        """
        Convert the given text to API format

        Converts: user mentions, channel mentions, role mentions and emojis
        """
        text = text.replace(">", "\u200b>")
        await ctx.send(f"**API Format**```\n{text}\n```")

    @cmd.command()
    @cmd.guild_only()
    @cmd.has_permissions(manage_webhooks=True)
    @cmd.bot_has_permissions(manage_webhooks=True)
    async def webhook(self, ctx, channel=None):
        """
        Get a webhook for the current channel

        Re-uses an existing webhook if available
        """
        if channel is not None:
            channel_regex = f"(<#)?([0-9]+)>?"
            channel_match = re.match(channel_regex, channel)
            if channel_match is None:
                await ctx.send("Invalid channel id or mention provided")
                return

            channel = ctx.guild.get_channel(int(channel_match[2]))
            if channel is None:
                await ctx.send("Unknown channel. The channel must belong to this guild.")
                return

        else:
            channel = ctx.channel

        existing_webhooks = await channel.webhooks()
        if len(existing_webhooks) > 0:
            await ctx.send(f"**Using one of the existing Webhooks**:```{existing_webhooks[0].url}```")
            return

        new_webhook = await channel.create_webhook(name="discord.club")
        await ctx.send(f"**Created a new Webhook**:```{new_webhook.url}```")

    async def _get_message_json(self, ctx, message_id_or_url):
        url_regex = r"https:\/\/(canary\.)?discord(app)?.com\/channels\/[0-9]+\/([0-9]+)\/([0-9]+)\/?"
        url_match = re.match(url_regex, message_id_or_url)
        msg_id = message_id_or_url
        channel = ctx.channel
        if url_match:
            channel = ctx.guild.get_channel(int(url_match[3]))
            msg_id = int(url_match[4])

        try:
            msg_id = int(msg_id)
        except ValueError:
            return None

        if channel is None:
            return None

        try:
            msg = await channel.fetch_message(msg_id)
        except discord.NotFound:
            return None

        return {
            "username": msg.author.name,
            "avatar_url": str(msg.author.avatar_url) if msg.author.avatar_url else None,
            "content": msg.content,
            "embeds": [e.to_dict() for e in msg.embeds],
            "tts": msg.tts
        }

    async def _create_share(self, data):
        share_id = uuid.uuid4().hex[:8]
        await self.bot.redis.setex(f"share:{share_id}", 60 * 60 * 24, json.dumps(data))
        return f"{self.bot.site_host}/share/{share_id}"

    @cmd.command(name="json", aliases=("code",))
    @cmd.guild_only()
    @cmd.has_permissions(manage_messages=True)
    @cmd.bot_has_permissions(read_message_history=True)
    async def _json(self, ctx, message_id_or_url):
        """
        Get the json code for a given message in the current channel
        """
        data = await self._get_message_json(ctx, message_id_or_url)
        if data is None:
            await ctx.send(f"Unknown message. The message must be in the channel that belongs to this server.")
            return

        try:
            await ctx.send(f"**JSON Code**```js\n{json.dumps(data)}\n```")
        except discord.HTTPException:
            share_url = await self._create_share(data)
            embed = discord.Embed(
                title="Edit Message",
                description=f"You can view and edit the message [here](<{share_url}>)\n\n"
                            f"*This link will be valid for 24 hours*"
            )
            await ctx.send(embed=embed)

    @cmd.command()
    @cmd.guild_only()
    @cmd.has_permissions(manage_messages=True)
    @cmd.bot_has_permissions(read_message_history=True)
    async def edit(self, ctx, message_id_or_url):
        """
        Get a share link for a given message in the current channel
        """
        data = await self._get_message_json(ctx, message_id_or_url)
        if data is None:
            await ctx.send(f"Unknown message. The message must be in the channel that belongs to this server.")
            return

        share_url = await self._create_share(data)
        embed = discord.Embed(
            title="Edit Message",
            description=f"You can view and edit the message [here](<{share_url}>)\n\n"
                        f"*This link will be valid for 24 hours*"
        )
        await ctx.send(embed=embed)

    @cmd.command(aliases=("website", "use", "support", "invite", "discord"))
    async def info(self, ctx):
        """
        Website, discord and invite link
        """
        embed = discord.Embed(
            title="Discord.Club",
            description="The easiest way to generate embeds and improve the look of your servers.\n\n"
                        "[Website](https://discord.club)"
                        " | [Invite](https://discord.club/invite)"
                        " | [Support Discord](https://discord.club/discord)"
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utilities(bot))
