from sanic import Blueprint, response
import bson
from enum import IntEnum

from utils import *
from auth import requires_token


bp = Blueprint(name="api.platforms", url_prefix="/platforms")


class PlatformType(IntEnum):
    DISCORD_BOT = 0


def validate_platform_values(type, values):
    if type == PlatformType.DISCORD_BOT:
        required = ("token", "public_key")
        for key in required:
            if key not in values.keys():
                return False

        return True

    return False


@bp.post("/")
@requires_token
@requires_body(
    type=PlatformType,
    name=str,
    values=dict
)
async def create_platform(request, payload, user_id):
    validate_platform_values(payload["type"], payload["values"])

    data = {
        "type": payload["type"].value,
        "name": payload["name"],
        "values": payload["values"]
    }
    result = await request.app.db.platforms.insert_one({
        "user_id": user_id,
        **data
    })
    return response.json({
        "id": str(result.inserted_id),
        **data
    })


@bp.get("/<platform_id>")
@requires_token
async def get_platform(request, user_id, platform_id):
    try:
        platform_id = bson.ObjectId(platform_id)
    except bson.errors.InvalidId:
        return response.empty(status=404)

    data = await request.app.db.platforms.find_one({"user_id": user_id, "_id": platform_id})
    if data is None:
        return response.empty(status=404)

    data["id"] = str(data.pop("_id"))
    del data["user_id"]
    return response.json(data)


@bp.patch("/<platform_id>")
@requires_token
@requires_body(
    name=str,
    values=dict
)
async def update_platform(request, payload, user_id, platform_id):
    existing = await request.app.db.platforms.find_one({"_id": platform_id, "user_id": user_id})
    if existing is None:
        return response.empty(status=404)

    type = PlatformType(existing["type"])
    validate_platform_values(type, payload["values"])

    try:
        platform_id = bson.ObjectId(platform_id)
    except bson.errors.InvalidId:
        return response.empty(status=404)

    data = {
        "name": payload["name"],
        "values": payload["values"]
    }

    await request.app.db.platforms.update_one(
        {"user_id": user_id, "_id": platform_id},
        {"$set": data}
    )

    return response.json({
        "id": platform_id,
        "type": type.value,
        **data
    })


@bp.delete("/<platform_id>")
@requires_token
async def delete_platform(request, user_id, platform_id):
    try:
        platform_id = bson.ObjectId(platform_id)
    except bson.errors.InvalidId:
        return response.empty(status=404)

    await request.app.db.platforms.delete_one({"user_id": user_id, "_id": platform_id})
    return response.json({"id": str(platform_id)})
