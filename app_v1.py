from flask import Flask, request, render_template_string
app = Flask(__name__)

server_data = {}

HTML_TEMPLATE = """
<html>
<head>
    <title>Roblox Server Movement Monitor</title>
    <style>
        body { font-family: Arial; background-color: #111; color: white; }
        .red { background: #400; padding: 10px; border-radius: 6px; }
        .green { background: #040; padding: 10px; border-radius: 6px; }
        a { color: white; }
    </style>
</head>
<body>
    <h1>Roblox Server Movement Monitor</h1>
    <ul>
    {% for s, info in server_data.items() %}
        <li class="{{ 'red' if info.moving else 'green' }}">
            <a href="{{ info.url }}" target="_blank">{{ info.url }}</a><br>
            Players moving: {{ info.moving }}<br>
            {{ info.players }}
        </li>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/report", methods=["POST"])
def report():
    data = request.json
    sid = data.get("serverId")
    gid = data.get("gameId")
    players = data.get("players", {})
    any_moving = any(players.values())
    url = f"https://www.roblox.com/games/{gid}"
    server_data[sid] = {"url": url, "moving": any_moving, "players": players}
    return "ok"

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, server_data=server_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
