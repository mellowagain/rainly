from flask import Blueprint
from flask import Response
from flask import request
from flask import abort
import simplejson as json
import requests

# https://circleci.com/
# https://circleci.com/docs/1.0/configuration/#notify

blueprint = Blueprint("CircleCI", "circle")

@blueprint.route("/circle/<string:unique_id>/<string:secret>", methods=["POST"])
def circle_ci(unique_id, secret):
    # Webhook will look like this:
    # https://canary.discordapp.com/api/webhooks/<unique_id>/<secret>

    payload = request.get_json(force=True, cache=False)

    if str(payload["payload"]["outcome"]) != "success":
        color = 0xFF0000  # Failure - Red
    else:
        color = 0x008000  # Success - Green

    discord_payload = json.dumps(
        {
            "username": "Circle CI",
            "avatar_url": "https://a.slack-edge.com/7f1a0/plugins/circleci/assets/service_512.png",
            "embeds": [
                {
                    "title": "Build #" + str(payload["payload"]["build_num"]),
                    "description": "`" + str(payload["payload"]["vcs_revision"])[0:7] + "`: " +
                                         str(payload["payload"]["status"]).replace("_", ""),
                    "url": payload["payload"]["build_url"],
                    "color": color,
                    "author": {
                        "name": payload["payload"]["reponame"],
                        "url": payload["payload"]["vcs_url"]
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
