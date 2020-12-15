from sanic import Blueprint, response
from enum import IntEnum
from datetime import datetime
import bson

from utils import *
from stay_fast import *
from auth import requires_token


bp = Blueprint(name="api.triggers", url_prefix="/triggers")


"""
An trigger is composed of a trigger type (and settings for that trigger type) and a list of actions.
Different trigger types have different settings and different actions take different arguments.
"""


class TriggerType(IntEnum):
    SCHEDULED = 0
    CUSTOM_COMMAND = 1


class ActionType(IntEnum):
    EXECUTE_WEBHOOK = 0
    EXECUTE_WEBHOOK_EDIT = 1
    COMMAND_RESPONSE = 2


def parse_settings(type, settings):
    if type == TriggerType.SCHEDULED:
        return {
            "start": datetime.fromtimestamp(float(settings["start_timestamp"])),
            "repeat": float(settings["repeat"])  # just the seconds between each trigger execution
        }

    elif type == TriggerType.CUSTOM_COMMAND:
        return {
            "command_id": str(settings["command_id"]),
            "public_key": str(settings["public_key"])
        }


def parse_actions(actions):
    """
    Errors are not handled and just raised to the caller
    """
    if not isinstance(actions, list):
        raise ValueError

    result = []
    for action in actions:
        type = ActionType(action["type"])
        if type == ActionType.EXECUTE_WEBHOOK:
            result.append({
                "type": type,
                "webhook_id": str(action["webhook_id"]),
                "webhook_token": str(action["webhook_token"]),
                "message_id": str(action["message_id"]),
                "message_variables": list(action["message_variables"])
            })

        elif type == ActionType.EXECUTE_WEBHOOK_EDIT:
            result.append({
                "type": type,
                "webhook_id": str(action["webhook_id"]),
                "webhook_token": str(action["webhook_token"]),
                "message_id": str(action["message_id"]),
                "message_variables": list(action["message_variables"]),
                "discord_message_id": str(action["discord_message_id"]),
            })

        elif type == ActionType.COMMAND_RESPONSE:
            result.append({
                "type": type,
                "response_flags": int(action["response_flags"]),
                "response_type": int(action["response_type"]),
                "message_id": str(action["message_id"]),
                "message_variables": list(action["message_variables"])
            })

    return result


@bp.post("/")
@requires_body(
    type=TriggerType,
    name=str,
    settings=dict,
    actions=parse_actions
)
@requires_token
@ratelimit(limit=2, seconds=5)
async def create_trigger(request, user_id, payload):
    try:
        settings = parse_settings(payload["type"], payload.pop("settings"))
    except:
        return response.json({"error": "Invalid value for field 'settings'"}, status=400)

    result = await request.app.db.insert_one({
        **payload,
        "user_id": user_id,
        "settings": settings
    })
    return response.json({"id": result.inserted_id})


@bp.post("/<trigger_id>")
@requires_body(
    type=TriggerType,
    name=str,
    settings=dict,
    actions=parse_actions
)
@requires_token
@ratelimit(limit=2, seconds=5)
async def update_trigger(request, user_id, trigger_id, payload):
    try:
        settings = parse_settings(payload["type"], payload.pop("settings"))
    except:
        return response.json({"error": "Invalid value for field 'settings'"}, status=400)

    try:
        trigger_id = bson.ObjectId(trigger_id)
    except bson.errors.InvalidId:
        return response.json({"error": "Invalid trigger ID"}, status=404)

    result = await request.app.db.update_one({"_id": trigger_id}, {"$set": {
        **payload,
        "settings": settings
    }})
    if result.updated_count == 0:
        return response.json({"error": "Unknown trigger"}, status=400)

    return response.json({})


@bp.get("/")
@requires_token
@ratelimit(limit=2, seconds=5)
async def get_triggers(request, user_id):
    pass


@bp.get("/<trigger_id>")
@requires_token
@ratelimit(limit=3, seconds=5)
async def get_trigger(request, user_id, trigger_id):
    pass


@bp.get("/find")
@requires_token
@ratelimit(limit=30, seconds=30)
async def find_trigger(request, user_id, trigger_token):
    """
    accepts a trigger secret or a command-id (for custom commands)
    """
    pass


@bp.delete("/<trigger_id>")
@requires_token
@ratelimit(limit=2, seconds=5)
async def delete_trigger(request, user_id, trigger_id):
    pass
