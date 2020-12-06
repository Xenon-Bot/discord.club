from sanic import Blueprint

from . import oauth, messages

bp = Blueprint.group(oauth.bp, messages.bp)


async def setup(app):
    for sub in {oauth, messages}:
        try:
            await sub.setup(app)
        except AttributeError:
            pass
