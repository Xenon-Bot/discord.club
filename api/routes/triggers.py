from sanic import Blueprint, response
from sanic.exceptions import abort
from enum import IntEnum
from datetime import datetime, timedelta
import bson
import traceback
import json
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import dc_interactions as dc
import asyncio

from utils import *
from stay_fast import *
from auth import requires_token
from .integrations import IntegrationType

bp = Blueprint(name="api.triggers", url_prefix="/triggers")

"""
An trigger is composed of a trigger type (and settings for that trigger type) and a list of actions.
Different trigger types have different settings and different actions take different arguments.
"""


class TriggerType(IntEnum):
    SCHEDULED = 0
    CUSTOM_COMMAND = 1
    TWITCH = 2


class ActionType(IntEnum):
    EXECUTE_WEBHOOK = 0
    EXECUTE_WEBHOOK_EDIT = 1
    COMMAND_RESPONSE = 2


def parse_settings(type, settings):
    if type == TriggerType.SCHEDULED:
        return {
            "next": datetime.fromtimestamp(float(settings["next"])),
            "repeat": float(settings["repeat"])  # just the seconds between each trigger execution
        }

    elif type == TriggerType.CUSTOM_COMMAND:
        return {
            "command_id": str(settings["command_id"]),
            "show_source": bool(settings["show_source"]),
            "integration_id": str(settings["integration_id"])
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
                "response_ephemeral": bool(action["response_ephemeral"]),
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
        abort(400, "Invalid value for field 'settings'")

    result = await request.app.db.triggers.insert_one({
        "user_id": user_id,
        "type": payload["type"],
        "name": payload["name"],
        "settings": settings,
        "actions": payload["actions"],
        "logs": []
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
        raise abort(400, "Invalid value for field 'settings'")

    try:
        trigger_id = bson.ObjectId(trigger_id)
    except bson.errors.InvalidId:
        raise abort(404, "Invalid trigger ID")

    result = await request.app.db.triggers.update_one({"_id": trigger_id, "user_id": user_id}, {"$set": {
        **payload,
        "settings": settings
    }})
    if result.updated_count == 0:
        raise abort(400, "Unknown trigger")

    return response.json({})


@bp.get("/")
@requires_token
@ratelimit(limit=2, seconds=5)
async def get_triggers(request, user_id):
    triggers = []
    async for trigger in request.app.db.triggers.find({"user_id": user_id}):
        del trigger["user_id"]
        triggers.append({
            "id": str(trigger.pop("_id")),
            **trigger
        })

    return response.json(triggers)


@bp.get("/<trigger_id>")
@requires_token
@ratelimit(limit=3, seconds=5)
async def get_trigger(request, user_id, trigger_id):
    try:
        trigger_id = bson.ObjectId(trigger_id)
    except bson.errors.InvalidId:
        abort(404, "Invalid trigger ID")

    result = await request.app.db.triggers.find_one({"_id": trigger_id, "user_id": user_id})
    if result is None:
        abort(404, "Unknown trigger")

    result["id"] = str(result.pop("_id"))
    del result["user_id"]
    return response.json(result)


@bp.delete("/<trigger_id>")
@requires_token
@ratelimit(limit=2, seconds=5)
async def delete_trigger(request, user_id, trigger_id):
    try:
        trigger_id = bson.ObjectId(trigger_id)
    except bson.errors.InvalidId:
        abort(404, "Invalid trigger ID")

    await request.app.db.triggers.delete_one({"_id": trigger_id, "user_id": user_id})
    return response.json({})


@bp.post("/discord/<client_id>")
@ratelimit(limit=10, seconds=10)
async def discord_entry(req, client_id):
    raw_data = req.body.decode("utf-8")
    signature = req.headers.get("x-signature-ed25519")
    timestamp = req.headers.get("x-signature-timestamp")
    if signature is None or timestamp is None:
        raise abort(401)

    integration = await req.app.db.integrations.find_one({
        "type": IntegrationType.DISCORD_BOT.value,
        "values.client_id": client_id
    })
    if integration is None:
        raise abort(404, "Unknown client id")

    values = integration["values"]
    try:
        public_key = VerifyKey(bytes.fromhex(values["public_key"]))
    except:
        raise abort(401, "Integration public key is invalid")

    try:
        public_key.verify(f"{timestamp}{raw_data}".encode(), bytes.fromhex(signature))
    except BadSignatureError:
        raise abort(401, "Invalid signature")

    if not integration.get("validated"):
        await req.app.db.integrations.update_one({"_id": integration["_id"]}, {"$set": {"validated": True}})

    data = dc.InteractionPayload(json.loads(raw_data))
    resp = await discord_interaction_receive(req.app, client_id, data)
    if resp is None:
        resp = dc.InteractionResponse.ack()

    return response.json(resp.to_dict())


async def discord_interaction_receive(app, client_id, payload):
    if payload.type == dc.InteractionType.PING:
        return dc.InteractionResponse.pong()

    elif payload.type == dc.InteractionType.APPLICATION_COMMAND:
        trigger = await app.db.triggers.find_one({"settings.command_id": payload.data.id})
        if trigger is None:
            return dc.InteractionResponse.message("Unknown Command! :(", ephemeral=True)

        app.loop.create_task(run_trigger(app, trigger, interaction=payload, client_id=client_id))
        if trigger["settings"].get("show_source"):
            return dc.InteractionResponse.ack_with_source()

        return dc.InteractionResponse.ack()


async def outbound_request(app, method, url, data=None):
    async with app.session.request(
            method=method,
            url=url,
            json=data
    ) as resp:
        return resp


async def run_action(app, trigger, action, **context):
    if action["type"] == ActionType.COMMAND_RESPONSE:
        if trigger["type"] != TriggerType.CUSTOM_COMMAND:
            return

        interaction = context["interaction"]
        client_id = context["client_id"]
        message = await app.db.messages.find_one({"_id": action["message_id"]})
        await outbound_request(
            app,
            "POST",
            f"https://discord.com/api/webhooks/{client_id}/{interaction.token}",
            data={
                "flags": 1 << 6 if action["response_ephemeral"] else 0,
                **message["json"]
            }
        )

    elif action["type"] == ActionType.EXECUTE_WEBHOOK:
        message = await app.db.messages.find_one({"_id": action["message_id"]})
        await outbound_request(
            app,
            "POST",
            f"https://discord.com/api/webhooks/{action['webhook_id']}/{action['webhook_token']}",
            data=message["json"]
        )

    elif action["type"] == ActionType.EXECUTE_WEBHOOK_EDIT:
        pass


async def run_trigger(app, trigger, **context):
    log_entries = []
    for a, action in enumerate(trigger["actions"]):
        try:
            await run_action(app, trigger, action, **context)
        except:
            traceback.print_exc()
            log_entries.append(f"Action {a + 1} failed with an error")

        else:
            log_entries.append(f"Action {a + 1} succeeded")

    await app.db.triggers.update_one({"_id": trigger["_id"]}, {
        "$push": {
            "logs": {
                "$each": [{"timestamp": datetime.utcnow(), "entries": log_entries}],
                "$slice": -10
            }
        }
    })


async def schedule_loop(app):
    while True:
        await asyncio.sleep(10)
        try:
            async for trigger in app.db.triggers.find({
                "type": TriggerType.SCHEDULED,
                "settings.next": {"$lte": datetime.utcnow()}
            }):
                await app.db.triggers.update_one({"_id": trigger["_id"]}, {"$set": {
                    "settings.next": datetime.utcnow() + timedelta(seconds=trigger["settings"]["repeat"])
                }})
                app.loop.create_task(run_trigger(app, trigger))
        except:
            traceback.print_exc()


async def setup(app):
    app.loop.create_task(schedule_loop(app))
