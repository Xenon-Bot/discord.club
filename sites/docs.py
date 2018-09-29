from aiohttp import web
import aiohttp_jinja2 as jinja2


routes = web.RouteTableDef()
base = "/docs"


@routes.get(base)
async def discord(request):
    return jinja2.render_template("/docs/index.html", request, {})

@routes.get(base + "/xenon")
async def discord(request):
    raise web.HTTPFound("https://docs.discord.club/xenon/")
    #return jinja2.render_template("/docs/xenon.html", request, {})

@routes.get(base + "/embed-generator")
async def discord(request):
    raise web.HTTPFound("https://docs.discord.club/embed-generator/")
    #return jinja2.render_template("/docs/embed_generator.html", request, {})


async def setup(application):
    application.add_routes(routes)