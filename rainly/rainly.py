from modules import appveyor
from modules import travisci
from modules import circleci
from modules import vsts
from flask import Flask
import sys

# Flask is handling everything
app = Flask("rainly")

if __name__ == "__main__":
    if len(sys.argv) != 2:  # The first argument is always the script itself
        print("Usage: rainly <port>")
        exit(-1)

    host = None
    port = 0

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Please provide a a valid port as integer.")
        exit(-1)

    app.register_blueprint(appveyor.blueprint)
    app.register_blueprint(travisci.blueprint)
    app.register_blueprint(circleci.blueprint)
    app.register_blueprint(vsts.blueprint)
    app.run(host="0.0.0.0", port=port)
