from aiohttp import web


routes = web.RouteTableDef()


@routes.get("/discord")
async def discord(request):
    raise web.HTTPFound("https://discord.gg/ZCMN7YP")

@routes.get("/git")
async def git(request):
    raise web.HTTPFound("https://github.com/Magic-Bots")

@routes.get("/donate")
async def donate(request):
    raise web.HTTPFound("https://donatebot.io/checkout/410488579140354049")

@routes.get("/invite/xenon")
async def xenon(request):
    raise web.HTTPFound("https://discordapp.com/api/oauth2/authorize?client_id=416358583220043796&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.club%2Fapi%2Fxenon%2Foauth%2Frejoin.php&scope=bot")

@routes.get("/invite/embed-generator")
async def embed_generator(request):
    raise web.HTTPFound("https://discordapp.com/api/oauth2/authorize?client_id=410138706490425344&permissions=0&redirect_uri=https%3A%2F%2Fdiscord.club%2Ftools%2Fembed-generator&response_type=code&scope=bot%20messages.read")


async def setup(application):
    app = application
    application.add_routes(routes)