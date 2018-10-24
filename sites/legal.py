from aiohttp import web
import aiohttp_jinja2 as jinja2


routes = web.RouteTableDef()


@routes.get("/imprint")
async def imprint(request):
    return jinja2.render_template("/legal/imprint.html", request, {})


@routes.get("/privacy")
async def privacy(request):
    return jinja2.render_template("/legal/privacy.html", request, {})


@routes.get("/cookies")
async def privacy(request):
    return jinja2.render_template("/legal/cookies.html", request, {})


async def setup(app):
    app.add_routes(routes)