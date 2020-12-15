from sanic import Blueprint

from . import oauth, messages, triggers

bp = Blueprint.group(oauth.bp, messages.bp, triggers.bp)


async def setup(app):
    for sub in {oauth, messages, triggers}:
        try:
            await sub.setup(app)
        except AttributeError:
            pass
