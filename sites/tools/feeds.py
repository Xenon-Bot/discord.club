from aiohttp import web
import aiohttp_jinja2 as jinja2
import discord
import json

routes = web.RouteTableDef()
base = "/tools/feeds"
app = None


@routes.get(base + "/")
async def index_slash(request):
    return await index(request)


@routes.get(base)
async def index(request):
    return jinja2.render_template("/tools/embed_generator/index.html", request, {})


async def setup(application):
    global app
    app = application
    application.add_routes(routes)
