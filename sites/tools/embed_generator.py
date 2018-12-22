from aiohttp import web
import aiohttp_jinja2 as jinja2
import discord
import aioauth_client
import secrets

routes = web.RouteTableDef()
base = "/tools/embed-generator"
app = None


def HTMLColorToRGB(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#':
        colorstring = colorstring[1:]

    if len(colorstring) != 6:
        raise ValueError("input #%s is not in #RRGGBB format" % colorstring)
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return (r, g, b)


@routes.get(base + "/")
async def index_slash(request):
    return await index(request)


@routes.get(base)
async def index(request):
    context = {}
    if request.query.get("code") is not None:
        try:
            oauth_client = aioauth_client.DiscordClient(client_id=410138706490425344,
                                                        client_secret=secrets.client_secret)
            token, data = await oauth_client.get_access_token(code=request.query.get("code"),
                                                              redirect_uri="https://discord.club/tools/embed-generator")
            context["webhook"] = "/".join(data["webhook"]["url"].split("/")[-2:])
        except:
            pass

    return jinja2.render_template("/tools/embed_generator/index.html", request, context)


@routes.post(base + "/process")
async def process(request):
    content = await request.post()
    fields = []
    i = 0
    while f"field_{i}_name" in content:
        fields.append({
            "name": content[f"field_{i}_name"],
            "value": content[f"field_{i}_value"],
            "inline": content.get(f"field_{i}_inline") is not None,
        })
        i += 1

    embed_data = {
        "title": content["title"],
        "description": content["description"],
        "url": content["url"],
        "timestamp": content["timestamp"],
        "footer": {
            "text": content["footer_text"],
            "icon_url": content["footer_icon"]
        },
        "image": {
            "url": content["image"]
        },
        "thumbnail": {
            "url": content["thumbnail"]
        },
        "author": {
            "name": content["author_name"],
            "url": content["author_url"],
            "icon_url": content["author_icon"]
        },
        "fields": fields,
    }
    embed = discord.Embed(color=discord.Color.from_rgb(*HTMLColorToRGB(content["color"])))
    raw_embed = embed.to_dict()
    raw_embed.update(embed_data)
    embed = discord.Embed.from_data(raw_embed)
    if embed.description == "" and embed.title == "" and embed.author.name == "" and \
            len(embed.fields) == 0 and embed.thumbnail.url == "" and \
            embed.image.url == "" and embed.footer.text == "":
        embed = None

    try:
        adapter = discord.AsyncWebhookAdapter(app["http_session"])
        webhook = discord.Webhook.from_url("https://discordapp.com/api/webhooks/" + content["webhook_url"],
                                           adapter=adapter)
        await webhook.send(embed=embed, content=content["content"],
                           username=content["webhook_name"], avatar_url=content["webhook_avatar"])

        log = discord.Webhook.from_url(request.app.secrets.embed_log, adapter=adapter)
        await log.send(embed=embed,
                       content=f"**Sended to:** https://discordapp.com/api/webhooks/{content['webhook_url']}",
                       username=content["webhook_name"], avatar_url=content["webhook_avatar"])
    except Exception as e:
        return jinja2.render_template("/tools/embed_generator/error.html", request, {"error": str(e)})

    return jinja2.render_template("/tools/embed_generator/success.html", request, {})


async def setup(application):
    global app
    app = application
    application.add_routes(routes)
