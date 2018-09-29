from aiohttp import web
import aiohttp_jinja2 as jinja2


routes = web.RouteTableDef()


@routes.get("/")
async def index(request):
    return jinja2.render_template("/index.html", request, {})


async def setup(app):
    app.add_routes(routes)