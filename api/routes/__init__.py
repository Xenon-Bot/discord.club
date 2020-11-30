from sanic import Blueprint

from . import oauth, platforms, messages, triggers

bp = Blueprint.group(oauth.bp, platforms.bp, triggers.bp, messages.bp, url_prefix="/api")


async def setup(app):
    for sub in {oauth, platforms, messages, triggers}:
        try:
            await sub.setup(app)
        except AttributeError:
            pass
