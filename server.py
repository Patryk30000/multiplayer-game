from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
import uuid

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

players = {}

@app.route("/")
def index():
    return send_from_directory(".", "client.html")

@socketio.on("connect")
def on_connect():
    player_id = str(uuid.uuid4())
    players[player_id] = {"x": 100, "y": 100}
    emit("init", {"id": player_id, "players": players})
    emit("system", f"Player {player_id[:5]} joined")
    emit("update", players, broadcast=True)

@socketio.on("move")
def on_move(data):
    pid = data["id"]
    if pid in players:
        players[pid]["x"] += data["dx"]
        players[pid]["y"] += data["dy"]
        emit("update", players, broadcast=True)

@socketio.on("chat")
def on_chat(data):
    msg = data["message"][:200]  # basic safety limit
    name = data["name"]
    emit("chat", {"name": name, "message": msg}, broadcast=True)

@socketio.on("disconnect")
def on_disconnect():
    emit("system", "A player disconnected", broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
