from sanic import Blueprint, response
from enum import IntEnum
import bson
import asyncio

from utils import *
from auth import requires_token

bp = Blueprint(name="api.triggers", url_prefix="/triggers")


class TriggerType(IntEnum):
    SLASH_COMMAND = 0
    TIME = 1
    INTERVAL = 2
    HTTP_STATUS = 3
    PING = 4
    WEBHOOK = 5


REQUIRED_DATA_FIELDS = {
    TriggerType.SLASH_COMMAND: {
        "day": int,
        "hour": int,
        "minute": int
    },
    TriggerType.TIME: {
        "day": int,
        "hour": int,
        "minute": int
    },
    TriggerType.INTERVAL: {
        "interval": int
    },
    TriggerType.HTTP_STATUS: {
        "endpoint": str
    },
    TriggerType.PING: {
        "ip": str
    },
    TriggerType.WEBHOOK: {}
}


def validate_trigger_data(type, data):
    required = REQUIRED_DATA_FIELDS[type]
    result = {}
    for key, converter in required.items():
        if key not in data.keys():
            return response.json({"error": f"Field 'data.{key}' is required"}, status=400)

        try:
            result[key] = converter(data[key])
        except:
            return response.json({"error": f"Invalid value for field 'data.{key}'"}, status=400)

    for key in data.keys():
        if key not in required.keys():
            del result[key]

    if type == TriggerType.INTERVAL:
        if data.get("interval", 0) < 60:
            return response.json({"error": "Field 'data.interval' must be greater than 60"}, status=400)

    return result


@bp.post("/")
@requires_token
@requires_body(
    type=TriggerType,
    template_id=bson.ObjectId,
    name=str,
    data=dict
)
async def create_trigger(request, payload, user_id):
    payload = validate_trigger_data(payload["type"], payload["data"])
    if isinstance(payload, response.HTTPResponse):
        return payload


async def trigger_task(app):
    while True:
        await asyncio.sleep(5)
        # Check for lazy triggers


async def setup(app):
    app.loop.create_task(trigger_task(app))
