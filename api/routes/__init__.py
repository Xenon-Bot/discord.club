from sanic import Blueprint

from . import oauth, messages, triggers, integrations

bp = Blueprint.group(oauth.bp, messages.bp, triggers.bp, integrations.bp)


async def setup(app):
    for sub in {oauth, messages, triggers, integrations}:
        try:
            await sub.setup(app)
        except AttributeError:
            pass
