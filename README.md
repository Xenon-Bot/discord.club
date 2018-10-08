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

## Hosting (windows)

These are steps to host this website yourself.

- Install [Python](https://www.python.org/downloads/) 3.6 or higher (including pip)
  - Be sure to select "customize installation" and select "Add Python to evironment variables"
  
- Clone this repository or download it as a zip and extract it

- Navigate to the extracted folder and add a file called `secrets.py` and put in the following lines. (Replace <webhook_url> with a valid discord webhook url)
  - `embed_log = "<webhook_url>"`
  
- If you don't have a seperate server (e.g. nginx):
  - Open the web.py file
  - Uncomment line 31 (remove the `#`)
  - Save the file
  
- Open the cmd, navigate in the directory of the website and run the following commands:
  - `python -m pip install requirements.txt`
  
- Run the web.py file with the `python web.py` command.
