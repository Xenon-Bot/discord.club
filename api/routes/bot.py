import dc_interactions as dc
from xenon import rest
from xenon.cmd import *
from sanic import Blueprint
from os import environ as env
import re
import json
import uuid
import asyncio

bot = dc.InteractionBot(
    token=env["BOT_TOKEN"],
    public_key=env["BOT_PUBLIC_KEY"],
    guild_id=env.get("BOT_GUILD_ID"),
    ctx_klass=CustomContext
)
http = None
redis = None
db = None

bp = Blueprint(name="api.bot", url_prefix="/entry")


@bp.post("/")
async def bot_entry(req):
    return await bot.sanic_entry(req)


@bot.command()
async def invite(ctx):
    """
    Invite the bot to your server
    """
    await ctx.respond(
        "Click [here](<https://discord.club/invite>) to invite the bot to your server.",
        ephemeral=True
    )


@bot.command()
async def support(ctx):
    """
    Join the official support server
    """
    await ctx.respond(
        "Click [here](<https://discord.club/discord>) to join the official support server.",
        ephemeral=True
    )


@bot.command()
async def website(ctx):
    """
    Get the link to the official website
    """
    await ctx.respond(
        "You can find the official website and dashboard at <https://discord.club>.",
        ephemeral=True
    )


@bot.command(
    extends=dict(
        channel=dict(
            description="The channel you want a webhook for"
        )
    )
)
@checks.cooldown(1, 3)
async def webhook(ctx, channel: dc.CommandOptionType.CHANNEL = None):
    """
    Get a valid webhook URL for this or another channel
    """
    channel_id = channel or ctx.channel_id
    try:
        channel = await http.get_channel(channel_id)
    except rest.HTTPNotFound:
        await ctx.respond_with_source(**create_message(
            "Unknown channel",
            f=Format.ERROR
        ))
        return

    webhooks = await http.get_channel_webhooks(channel)
    if len(webhooks) > 0:
        await ctx.respond_with_source(**create_message(
            f"<{webhooks[0].url}>",
            title="Existing Webhook",
            f=Format.SUCCESS
        ))
        return

    webhook = await http.create_webhook(channel, name="discord.club")
    await ctx.respond_with_source(**create_message(
        f"<{webhook.url}>",
        title="New Webhook",
        f=Format.SUCCESS
    ))


async def _get_message(ctx, message):
    channel_id = ctx.channel_id
    message_id = message

    url_regex = r"https:\/\/(canary\.)?discord(app)?.com\/channels\/[0-9]+\/([0-9]+)\/([0-9]+)\/?"
    url_match = re.match(url_regex, message)
    if url_match:
        channel_id = url_match.group(3)
        message_id = url_match.group(4)

    try:
        msg = await http.get_channel_message(channel_id, message_id)
    except rest.HTTPNotFound:
        return None, None

    return channel_id, msg


def _message_to_json(msg):
    return {
        "username": msg.author.name,
        "avatar_url": str(msg.author.avatar_url) if msg.author.avatar_url else None,
        "content": msg.content,
        "embeds": msg.embeds,
        "tts": msg.tts
    }


async def _create_share_link(data):
    share_id = uuid.uuid4().hex[:8]
    await redis.setex(f"share:{share_id}", 60 * 60 * 24, json.dumps(data))
    return f"https://discord.club/share/{share_id}"


@bot.command(
    name="json",
    extends=dict(
        message=dict(
            description="The ID or URL of the message"
        )
    )
)
@checks.cooldown(1, 3)
async def _json(ctx, message):
    """
    Get the json code for an existing message
    """
    await ctx.ack_with_source()
    await asyncio.sleep(0.2)

    channel_id, msg = await _get_message(ctx, message)
    if msg is None:
        await ctx.respond_with_source(**create_message(
            f"**Unknown message**. The message must be in a channel that belongs to this server.",
            f=Format.ERROR
        ))
        return

    await ctx.ack_with_source()
    await asyncio.sleep(0.2)

    msg_data = _message_to_json(msg)
    try:
        await ctx.respond_with_source(embeds=[dict(
            title="JSON Code",
            color=Format.INFO.color,
            description=f"```js\n{json.dumps(msg_data)}\n```"
        )])
    except:
        share_link = await _create_share_link({"json": msg_data})
        await ctx.respond_with_source(**create_message(
            f"The message is too big to send here. You can edit it using this link: {share_link}",
            title="Edit Message",
            f=Format.INFO
        ))


@bot.command(
    extends=dict(
        message=dict(
            description="The ID or URL of the message"
        )
    )
)
@has_permissions("manage_messages")
@bot_has_permissions("manage_webhooks")
@checks.cooldown(1, 5)
async def edit(ctx, message):
    """
    Get an existing message directly into the editor
    """
    await ctx.ack_with_source()
    await asyncio.sleep(0.2)

    channel_id, msg = await _get_message(ctx, message)
    if msg is None:
        await ctx.respond_with_source(**create_message(
            f"**Unknown message**. The message must be in a channel that belongs to this server.",
            f=Format.ERROR
        ))
        return

    message_url = None
    webhook_url = None
    if msg.webhook_id is not None:
        webhooks = await http.get_channel_webhooks(channel_id)
        for webhook in webhooks:
            if webhook.id == msg.webhook_id:
                webhook_url = webhook.url
                message_url = f"https://discord.com/api/v8/channels/{channel_id}/messages/{msg.id}"

    msg_data = _message_to_json(msg)
    share_link = await _create_share_link({
        "json": msg_data,
        "message_url": message_url,
        "webhook_url": webhook_url
    })
    await ctx.respond_with_source(**create_message(
        f"You can edit it using this link: {share_link}",
        title="Edit Message",
        f=Format.INFO
    ))


@bot.command()
async def format(ctx, text):
    """
    Format the given text as the API format (emojis & mentions)
    """
    text = text.replace(">", "\u200b>")
    await ctx.respond_with_source(**create_message(
        f"```{text}```",
        title="API Format",
        f=Format.INFO
    ))


@bot.command(
    extends=dict(
        title=dict(
            description="The title for the mini embed"
        ),
        description=dict(
            description="The description for the mini embed"
        ),
        url=dict(
            description="The url to redirect to when clicking on the mini embed"
        ),
        site_name=dict(
            description="The site name to display above the title"
        ),
        hex_color=dict(
            description="The color for the embed (e.g. #32a852)"
        ),
        image_url=dict(
            description="The URL to the image to display inside the embed"
        ),
        video_url=dict(
            description="The URL to the video to display inside the embed"
        )
    )
)
@checks.cooldown(1, 5)
async def mini(ctx, title, description, url=None, site_name=None, hex_color=None, image_url=None, video_url=None):
    """
    Create a mini embed that you can use everywhere
    """
    await ctx.ack_with_source()
    await asyncio.sleep(0.2)

    mini_id = uuid.uuid4().hex[:8]
    await db.minis.insert_one({
        "_id": mini_id,
        "title": title,
        "description": description,
        "url": url,
        "color": hex_color.strip("#") if hex_color else None,
        "site_name": site_name,
        "image_url": image_url,
        "video_url": video_url
    })
    await ctx.respond_with_source(**create_message(
        f"Successfully **created mini embed**. You can use it by sending this link into the discord chat:\n"
        f"<https://embed.gg/m/{mini_id}>",
        f=Format.SUCCESS
    ))


@bot.command(
    extends=dict(
        title=dict(
            description="The title for the mini embed"
        ),
        description=dict(
            description="The description for the mini embed"
        ),
        url=dict(
            description="The url to redirect to when clicking on the mini embed"
        ),
        hex_color=dict(
            description="The color for the embed (e.g. #32a852)"
        ),
        image_url=dict(
            description="The URL to the image to display inside the embed"
        ),
    )
)
@has_permissions("manage_messages")
@bot_has_permissions("manage_webhooks")
@checks.cooldown(1, 5)
async def embed(ctx, title, description, url=None, hex_color=None, image_url=None):
    """
    Create a simple embed and send them under your name
    """
    await ctx.ack_with_source()
    await asyncio.sleep(0.2)

    color = None
    if hex_color:
        hex_color = hex_color.strip("#")
        try:
            color = int(hex_color, 16)
        except ValueError:
            pass

    await ctx.ack()
    webhooks = await http.get_channel_webhooks(ctx.channel_id)
    if len(webhooks) == 0:
        webhook = await http.create_webhook(ctx.channel_id, name="discord.club")

    else:
        webhook = webhooks[0]

    await http.execute_webhook(
        webhook,
        username=ctx.author.name,
        avatar_url=str(ctx.author.avatar_url),
        embeds=[{
            "title": title,
            "description": description,
            "url": url,
            "color": color,
            "image": {"url": image_url}
        }]
    )


async def setup(app):
    global http
    global redis
    global db
    redis = app.redis
    ratelimits = rest.RedisRatelimitHandler(redis)
    http = rest.HTTPClient(env["BOT_TOKEN"], ratelimits)
    db = app.db

    await bot.session.close()
    bot.session = app.session
    bot.http = http
    bot.redis = redis
    await bot.prepare()
    # await bot.flush_commands()
    await bot.push_commands()
