from sanic import Blueprint, response
import bson
import pymongo
from datetime import datetime

from utils import *
from auth import requires_token


bp = Blueprint(name="api.messages", url_prefix="/messages")


@bp.post("/")
@requires_token
@requires_body(
    name=str,
    data=dict
)
async def create_template(request, payload, user_id):
    result = await request.app.db.templates.insert_one({
        "user_id": user_id,
        "name": payload["name"],
        "data": payload["data"]
    })
    return {
        "id": str(result.inserted_id),
        **payload
    }


@bp.patch("/<template_id>")
@requires_token
@requires_body()
async def update_template(request, payload, user_id, template_id):
    try:
        template_id = bson.ObjectId(template_id)
    except bson.errors.InvalidId:
        return response.empty(status=404)

    to_update = {}
    if "name" in payload:
        to_update["name"] = payload["name"]

    if "data" in payload:
        to_update["data"] = payload["data"]

    result = await request.app.db.templates.find_one_and_update(
        {"_id": template_id, "user_id": user_id},
        {"$set": to_update},
        return_document=pymongo.ReturnDocument.AFTER
    )
    result["id"] = result.pop("_id")
    del result["user_id"]
    return response.json(result)


@bp.delete("/<template_id>")
@requires_token
async def delete_template(request, user_id, template_id):
    try:
        template_id = bson.ObjectId(template_id)
    except bson.errors.InvalidId:
        return response.empty(status=404)

    await request.app.db.templates.delete_one({"_id": template_id, "user_id": user_id})
    return response.json({"id": template_id})


@bp.get("/<template_id>")
@requires_token
async def get_template(request, user_id, template_id):
    result = await request.app.db.templates.find_one({"_id": template_id, "user_id": user_id})
    result["id"] = result.pop("_id")
    del result["user_id"]
    return response.json(result)


@bp.get("/")
@requires_token
async def get_templates(request, user_id):
    return response.json([{"id": str(i), "name": f"Cool Message {i + 1}", "last_updated": datetime.utcnow().timestamp(), "data":
        {
            "content": "asdsadasdsadasdasdasdsadsadd",
            "embeds": [
                {
                    "title": "What's this?",
                    "color": 5814783,
                    "author": {},
                    "image": {},
                    "thumbnail": {},
                    "footer": {},
                    "fields": [
                        {
                            "name": "asdasd",
                            "value": "asd",
                            "inline": True
                        },
                        {
                            "name": "asd",
                            "value": "asd",
                            "inline": True
                        }
                    ]
                },
                {
                    "title": "cool embed",
                    "color": 16381952,
                    "description": "yeeeeetyeeeeetyeeeeetyeeeeetyeeeeetyeeeeetyeeeeetyeeeeetyeeeeetyeeeeetyeeeeetyeeeeet\nyeeeeetyeeeeetyeeeeet",
                    "author": {},
                    "image": {},
                    "thumbnail": {},
                    "footer": {}
                }
            ]
        }
    } for i in range(25)])
