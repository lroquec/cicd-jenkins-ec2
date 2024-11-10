import socket
from uuid import getnode as get_mac
from flask import Flask, jsonify
from flask_wtf import CSRFProtect


# Get device details
def get_device_details():
    hostname = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    MAC_address = get_mac()
    MAC_address = (
        ":".join(("%012X" % MAC_address)[i: i + 2] for i in range(0, 12, 2))
    ).replace(":", "-")
    return hostname, ip, MAC_address


app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)


# Returns device hostname,IP and MAC address
@app.route("/details")
def details():
    hostname, ip, mac = get_device_details()
    out = (
        "Hello!!!....I'm "
        + hostname
        + "....My MAC ID is "
        + mac
        + "....and My IP address is "
        + ip
    )
    return out


@app.route("/health")
def health():
    return jsonify(status="up")


@app.route("/")
def home():
    return """
        <html>
            <head>
                <title>Simple Python App</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        text-align: center;
                        margin-top: 50px;
                        background-color: #f0f0f0;
                    }
                    h1 {
                        color: #333;
                    }
                </style>
            </head>
            <body>
                <h1>Welcome to a very simple Python app!</h1>
            </body>
        </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
