from sanic import Blueprint

from . import oauth, messages, bot


to_load = {oauth, messages, bot}
bp = Blueprint.group(*[tl.bp for tl in to_load])


async def setup(app):
    for sub in to_load:
        try:
            await sub.setup(app)
        except AttributeError:
            pass
