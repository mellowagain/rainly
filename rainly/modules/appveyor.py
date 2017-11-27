from rainly import rainly
from flask import request
from flask import jsonify
from flask import abort
import simplejson as json
import requests

# https://www.appveyor.com/
# https://www.appveyor.com/docs/notifications/#webhooks

@rainly.app.route("/appveyor/<string:unique_id>/<string:secret>", methods="POST")
def appveyor(unique_id, secret):
    # Webhook will look like this:
    # https://canary.discordapp.com/api/webhooks/<unique_id>/<secret>

    payload = json.loads(request.args.get(""))

    color = 0

    if payload["eventData"]["passed"]:
        color = 0x008000  # Success - Green
    elif payload["eventData"]["failed"]:
        color = 0xFF0000  # Failure - Red
    else:
        color = 0x808080  # Unknown - Grey

    discord_payload = json.dumps(
        {
            "content": "embeds",
            "username": "Appveyor",
            "avatar_url": "https://www.appveyor.com/assets/img/appveyor-logo-256.png",
            "embeds": {
                "title": "Build " + payload["status"],
                "description": "`" + payload["commitId"] + "`: " + payload["status"],
                "url": payload["buildUrl"],
                "color": color
            }
        }
    )

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "rainly (https://github.com/Marc3842h/rainly)"
    }

    req = requests.post("https://canary.discordapp.com/api/webhooks/" + unique_id + "/" + secret,
                        json=discord_payload, headers=headers)
    if not req.ok:
        abort(500)
