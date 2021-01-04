from sanic import Blueprint, response
from sanic.exceptions import abort
import bson
import pymongo
import gridfs
from datetime import datetime
import json
import uuid

from utils import *
from stay_fast import *
from auth import requires_token


bp = Blueprint(name="api.messages", url_prefix="/messages")


@bp.post("/")
@requires_token
@ratelimit(limit=2, seconds=5)
async def save_message(request, user_id):
    data = single_value_form(request.form)
    if "name" not in data or "json" not in data:
        return response.json({}, status=400)

    file_count = 0
    file = request.files.get(f"file{file_count}")
    files = []
    while file is not None:
        file_id = await upload_file(request.app.file_bucket, file.name, file.body, file.type)
        files.append({"id": file_id, "name": file.name, "size": len(file.body)})

        file_count += 1
        file = request.files.get(f"file{file_count}")

    result = await request.app.db.messages.insert_one({
        "user_id": user_id,
        "last_updated": datetime.utcnow(),
        "name": data["name"],
        "json": json.loads(data["json"]),
        "files": files
    })
    return response.json({"id": str(result.inserted_id)})


@bp.patch("/<msg_id>")
@requires_token
@ratelimit(limit=2, seconds=5)
async def update_message(request, user_id, msg_id):
    try:
        msg_id = bson.ObjectId(msg_id)
    except bson.errors.InvalidId:
        return response.empty(status=404)

    data = single_value_form(request.form)
    if "json" not in data:
        return response.json({}, status=400)

    file_count = 0
    file = request.files.get(f"file{file_count}")
    files = []
    while file is not None:
        file_id = await upload_file(request.app.file_bucket, file.name, file.body, file.type)
        files.append({"id": file_id, "name": file.name, "size": len(file.body)})

        file_count += 1
        file = request.files.get(f"file{file_count}")

    await request.app.db.messages.update_one({"_id": msg_id}, {"$set": {
        "last_updated": datetime.utcnow(),
        "json": json.loads(data["json"]),
        "files": files
    }})
    return response.json({})


@bp.delete("/<msg_id>")
@requires_token
@ratelimit(limit=5, seconds=5)
async def delete_message(request, user_id, msg_id):
    try:
        msg_id = bson.ObjectId(msg_id)
    except bson.errors.InvalidId:
        return response.empty(status=404)

    await request.app.db.messages.delete_one({"_id": msg_id, "user_id": user_id})
    return response.json({})


@bp.get("/<msg_id>")
@requires_token
@ratelimit(limit=5, seconds=5)
# @cache_response(seconds=30)
async def get_message(request, user_id, msg_id):
    try:
        msg_id = bson.ObjectId(msg_id)
    except bson.errors.InvalidId:
        raise abort(404, "Invalid message ID")

    result = await request.app.db.messages.find_one({"_id": msg_id, "user_id": user_id})
    if result is None:
        raise abort(404, "Unknown message")

    result["id"] = str(result.pop("_id"))
    result["last_updated"] = result.pop("last_updated").timestamp()
    result["files"] = [{"id": str(f.pop("id")), **f} for f in result["files"]]
    del result["user_id"]
    return response.json(result)


@bp.get("/files/<file_id>")
@requires_token
@ratelimit(limit=5, seconds=5)
# @cache_response(seconds=60)
async def get_file(request, user_id, file_id):
    try:
        file_id = bson.ObjectId(file_id)
    except bson.errors.InvalidId:
        raise abort(404, "Invalid file ID")

    try:
        file = await request.app.file_bucket.open_download_stream(file_id)
    except gridfs.errors.NoFile:
        raise abort(404, "Unknown file ID provided")

    meta_data = file.metadata
    content_type = "application/octet-stream"
    if meta_data is not None and "content_type" in meta_data:
        content_type = meta_data["content_type"]

    resp = response.raw(
        await file.read(),
        content_type=content_type
    )
    return resp


@bp.get("/")
@requires_token
@ratelimit(limit=5, seconds=5)
# @cache_response(seconds=30)
async def get_messages(request, user_id):
    messages = []
    async for msg in request.app.db.messages.find({"user_id": user_id}, sort=[("last_updated", pymongo.DESCENDING)]):
        del msg["user_id"]
        messages.append({
            "id": str(msg.pop("_id")),
            "last_updated": msg.pop("last_updated").timestamp(),
            "files": [{"id": str(f.pop("id")), **f} for f in msg.pop("files")],
            **msg
        })

    return response.json(messages)


@bp.post("/share")
@requires_body(json=dict)
@ratelimit(limit=2, seconds=10, level=RequestBucket.IP)
async def create_share(request, payload):
    share_id = uuid.uuid4().hex[:8]
    await request.app.redis.setex(f"share:{share_id}", 60 * 60 * 24, json.dumps({
        "json": payload["json"]
    }))
    return response.json({"id": share_id})


@bp.get("/share/<share_id>")
@ratelimit(limit=5, seconds=5, level=RequestBucket.IP)
async def get_share(request, share_id):
    raw_share = await request.app.redis.get(f"share:{share_id}")
    if raw_share is None:
        raise abort(404, "Share does not exist or has expired")

    data = json.loads(raw_share)
    if "json" in data:
        return response.json(data)

    # legacy
    return response.json({"json": data})
