from sanic import Blueprint, response
from enum import IntEnum
import bson

from stay_fast import *
from utils import *
from auth import requires_token


class IntegrationType(IntEnum):
    DISCORD_BOT = 0


bp = Blueprint(name="api.integrations", url_prefix="/integrations")


def validate_values(type, values):
    if type == IntegrationType.DISCORD_BOT:
        client_id = values.get("client_id", "")
        bot_token = values.get("bot_token", "")
        public_key = values.get("public_key", "")

        if len(client_id) == 0:
            return response.json({"error": "The client id is required"}, status=404)

        if len(bot_token) == 0:
            return response.json({"error": "The bot token is required"}, status=404)

        if len(public_key) == 0:
            return response.json({"error": "the public key is required"}, status=404)

        return {
            "client_id": client_id,
            "bot_token": bot_token,
            "public_key": public_key
        }

    else:
        return response.json({"error": "Unknown integration type"}, status=404)


@bp.post("/")
@requires_body(name=str, type=IntegrationType, values=dict)
@requires_token
@ratelimit(limit=2, seconds=5)
async def create_integration(request, user_id, payload):
    name = payload["name"]
    if len(payload["name"]) < 3:
        return response.json({"error": "The integration name must be at least 3 characters long"}, status=404)

    values = validate_values(payload["type"], payload["values"])
    if isinstance(values, response.HTTPResponse):
        return values

    await request.app.db.integrations.insert_one({
        "user_id": user_id,
        "name": name,
        "type": payload["type"],
        "values": values
    })
    return response.json({})


@bp.get("/")
@requires_token
@ratelimit(limit=5, seconds=5)
async def get_integrations(request, user_id):
    result = []
    async for integration in request.app.db.integrations.find({"user_id": user_id}):
        result.append({
            "id": str(integration.pop("_id")),
            **integration
        })

    return response.json(result)


@bp.patch("/<integration_id>")
@requires_body(name=str, type=IntegrationType, values=dict)
@requires_token
@ratelimit(limit=2, seconds=5)
async def edit_integration(request, user_id, payload, integration_id):
    name = payload["name"]
    if len(payload["name"]) < 3:
        return response.json({"error": "The integration name must be at least 3 characters long"}, status=404)

    values = validate_values(payload["type"], payload["values"])
    if isinstance(values, response.HTTPResponse):
        return values

    try:
        integration_id = bson.ObjectId(integration_id)
    except bson.errors.InvalidId:
        return response.empty(status=404)

    await request.app.db.integrations.update_one({
        "_id": integration_id,
        "user_id": user_id,
    }, {"$set": {
        "name": name,
        "type": payload["type"],
        "values": values
    }})
    return response.json({})


@bp.delete("/<integration_id>")
@requires_token
@ratelimit(limit=2, seconds=5)
async def delete_integration(request, user_id, integration_id):
    try:
        integration_id = bson.ObjectId(integration_id)
    except bson.errors.InvalidId:
        return response.empty(status=404)

    await request.app.db.integrations.delete_one({"_id": integration_id, "user_id": user_id})
    return response.json({})
