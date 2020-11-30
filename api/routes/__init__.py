from sanic import Blueprint

from . import oauth, platforms, templates, triggers

bp = Blueprint.group(oauth.bp, platforms.bp, triggers.bp, templates.bp, url_prefix="/api")


async def setup(app):
    for sub in {oauth, platforms, templates, triggers}:
        try:
            await sub.setup(app)
        except AttributeError:
            pass
