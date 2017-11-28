from modules import appveyor
from modules import travisci
from flask import Flask
import sys

# Flask is handling everything
app = Flask("rainly")

if __name__ == "__main__":
    if len(sys.argv) != 3:  # The first argument is always the script itself
        print("Usage: rainly <host> <port>")
        exit(-1)

    host = None
    port = 0

    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
    except ValueError:
        print("Please provide a valid host as string and a valid port as integer.")
        exit(-1)

    app.register_blueprint(appveyor.blueprint)
    app.register_blueprint(travisci.blueprint)
    app.run(host=host, port=port)
