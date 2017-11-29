from flask import Blueprint
from flask import Response
from flask import request
from flask import abort
import simplejson as json
import requests

# https://www.appveyor.com/
# https://www.appveyor.com/docs/notifications/#webhooks

blueprint = Blueprint("AppVeyor", "appveyor")

@blueprint.route("/appveyor/<unique_id>/<secret>", methods=["POST"])
def appveyor(unique_id, secret):
    # Webhook will look like this:
    # https://canary.discordapp.com/api/webhooks/<unique_id>/<secret>

    payload = request.get_json(force=True, cache=False)

    color = 0

    if payload["eventData"]["passed"]:
        color = 0x008000  # Success - Green
    elif payload["eventData"]["failed"]:
        color = 0xFF0000  # Failure - Red
    else:
        color = 0x808080  # Unknown - Grey

    discord_payload = json.dumps(
        {
            "username": "Appveyor",
            "avatar_url": "https://www.appveyor.com/assets/img/appveyor-logo-256.png",
            "embeds": [
                {
                    "title": "Build #" + payload["buildNumber"],
                    "description": "`" + payload["commitId"] + "`: " + payload["status"],
                    "url": payload["buildUrl"],
                    "color": color,
                    "author": {
                        "name": str(payload["repositoryName"]).split("/")[1],
                        "url": payload["buildUrl"]  # Appveyor doesn't provide the actual repo url, so we use build url
                    }
                }
            ]
        }
    )

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "rainly (https://github.com/Marc3842h/rainly)"
    }

    req = requests.post("https://canary.discordapp.com/api/webhooks/" + unique_id + "/" + secret,
                        data=discord_payload, headers=headers)
    if not req.ok:
        abort(req.status_code)

    return Response(req.content, status=200, mimetype="application/json")
