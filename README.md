# Discord.club

Includes the homepage and all bots and tools on discord.club

## Dependencies

- [Python 3.6 or higher](https://www.python.org/)
- [Aiohttp 3.3.2 or higher](https://github.com/aio-libs/aiohttp/)
- [Jinja2 2.10](https://github.com/pallets/jinja)
- [Aiohttp_Jinja2 1.0](https://github.com/aio-libs/aiohttp-jinja2)

## Static Files

The static files are separately hosted on nginx, by default. If you want aiohttp to handle them, just uncomment [line 31 in web.py](https://github.com/Merlintor/Discord.club/edit/master/web.py#L31) .

## Secrets.py

The secrets.py file mentioned in [web.py](https://github.com/Merlintor/Discord.club/edit/master/web.py#L6) contains:

- embed_log -> webhook url for the embed log 
