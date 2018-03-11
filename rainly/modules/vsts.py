from flask import Blueprint
from flask import Response
from flask import request
from flask import abort
import simplejson as json
import requests

# https://www.visualstudio.com/team-services/
# https://docs.microsoft.com/en-us/vsts/service-hooks/services/webhooks

blueprint = Blueprint("Visual Studio Team Services", "vsts")

@blueprint.route("/vsts/<string:unique_id>/<string:secret>", methods=["POST"])
def travis_ci(unique_id, secret):
    # Webhook will look like this:
    # https://canary.discordapp.com/api/webhooks/<unique_id>/<secret>

    payload = request.get_json(force=True, cache=False)

    if "succeeded" in str(payload["message"]["text"]):
        color = 0x008000  # Success - Green
    else:
        color = 0xFF0000  # Failure - Red

    discord_payload = json.dumps(
        {
            "username": "Visual Studio Team Services",
            "avatar_url": "https://ms-vsts.gallerycdn.vsassets.io/extensions/ms-vsts/team/1.122.0/1502737672963/Microsoft.VisualStudio.Services.Icons.Default",
            "embeds": [
                {
                    "title": "Build #" + str(payload["resource"]["id"]),
                    "description": str(payload["resource"]["status"]),
                    "url": payload["resource"]["url"],
                    "color": color,
                    "author": {
                        "name": payload["resource"]["definition"]["name"],
                        "url": payload["resource"]["definition"]["url"]
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

