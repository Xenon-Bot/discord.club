from aiohttp import web, ClientSession
import aiohttp_jinja2, jinja2
import os
import json

import secrets
from sites import index, links, docs, errors
from sites.tools import embed_generator


startup_sites = [index, links, docs, embed_generator, errors]


async def prepare(app):
    app["http_session"] = ClientSession()
    app.secrets = secrets

    for file in os.listdir("./contents/data"):
        if not file.endswith(".json"):
            continue

        with open("./contents/data/" + file) as f:
            app[file.split(".")[0]] = json.load(f)

    for site in startup_sites:
        await site.setup(app)


app = web.Application()
app.on_startup.append(prepare)
#app.router.add_static('/static', "./static")
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("./contents/templates"))
web.run_app(app, port=8081)
