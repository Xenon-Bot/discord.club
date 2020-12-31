from sanic import Blueprint, response
from enum import IntEnum
import bson

from stay_fast import *
from utils import *
from auth import requires_token


class IntegrationType(IntEnum):
    DISCORD_BOT = 0


bp = Blueprint(name="api.integrations", url_prefix="/integrations")


@bp.post("/")
@requires_body(name=str, type=IntegrationType, values=dict)
@requires_token
@ratelimit(limit=2, seconds=5)
async def create_integration(request, user_id, payload):
    await request.app.db.integrations.insert_one({
        "user_id": user_id,
        "name": payload["name"],
        "type": payload["type"],
        "values": payload["values"]
    })
    return response.json({})


@bp.get("/")
@requires_token
@ratelimit(limit=2, seconds=5)
async def get_integrations(request, user_id):
    result = []
    async for integration in request.app.db.integrations.find({"user_id": user_id}):
        result.append({
            "id": str(integration.pop("_id")),
            **integration
        })

    return response.json(result)


@bp.patch("/<integration_id>")
@requires_token
@ratelimit(limit=2, seconds=5)
async def edit_integration(request, user_id, integration_id):
    try:
        integration_id = bson.ObjectId(integration_id)
    except bson.errors.InvalidId:
        return response.empty(status=404)


@bp.delete("/<integration_id>")
@requires_token
@ratelimit(limit=2, seconds=5)
async def delete_integration(request, user_id, integration_id):
    pass
