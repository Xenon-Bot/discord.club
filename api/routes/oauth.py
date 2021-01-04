from sanic import Blueprint, response
from sanic.exceptions import abort
import aiohttp

from utils import *
from stay_fast import *
from auth import requires_token


bp = Blueprint(name="api.oauth", url_prefix="/oauth")


@bp.post("/exchange")
@requires_body("code")
@ratelimit(limit=1, seconds=3, level=RequestBucket.IP)
async def exchange_token(request, payload):
    code = payload["code"]
    try:
        token = await request.app.exchange_token(code)
    except aiohttp.ClientResponseError as e:
        raise abort(e.status, f"Discord Exchange Error: '{e.message}'")

    if type(token) == bytes:
        token = token.decode()

    return response.json({"token": token})


@bp.get("/user")
@requires_token
@ratelimit(limit=1, seconds=3)
async def get_user(request, user_id):
    session = await request.app.db.sessions.find_one({"_id": user_id})
    return response.json(session["user"])


@bp.get("/tokens")
@requires_token
@ratelimit(limit=1, seconds=3)
async def get_tokens(request, user_id):
    session = await request.app.db.sessions.find_one({"_id": user_id})
    return response.json(session["tokens"])
