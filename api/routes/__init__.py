from sanic import Blueprint

from . import oauth, messages, bot, others, integrations, triggers


to_load = {oauth, messages, bot, others, integrations, triggers}
bp = Blueprint.group(*[tl.bp for tl in to_load])


async def setup(app):
    for sub in to_load:
        try:
            await sub.setup(app)
        except AttributeError:
            pass
