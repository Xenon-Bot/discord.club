from sanic import Blueprint, response

from stay_fast import *


bp = Blueprint(name="api.others", url_prefix="/")


@bp.get("/mini/<mini_id>")
@cache_response(seconds=5)
async def mini_embed(req, mini_id):
    mini = await req.app.db.minis.find_one({"_id": mini_id})

    if mini is None:
        return response.redirect("https://discord.club")

    meta = [
        f"<meta property='og:title' content='{mini['title']}'/>",
        f"<meta property='og:description' content='{mini['description']}'/>",
        f"<meta property='og:url' content='{mini['url']}'/>"
    ]

    if mini.get("site_name"):
        meta.append(f"<meta property='og:site_name' content='{mini['site_name']}'/>")

    if mini.get("image_url"):
        meta.append(f"<meta property='og:image' content='{mini['image_url']}'/>")

    if mini.get("video_url"):
        meta.append("<meta property='og:type' content='video.movie'/>")
        meta.append(f"<meta property='og:video' content='{mini['video_url']}'/>")

    if mini.get("color"):
        meta.append(f"<meta property='theme-color' content='#{mini['color']}'/>")

    script = f"window.onload = () => window.location.replace('{mini['url']}')"

    return response.html(f"<html><head>{''.join(meta)}<script>{script}</script></head></html>")
