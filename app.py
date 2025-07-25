from flask import Flask, render_template
from flask_socketio import SocketIO

from serial_reader import read_serial, simulate_info

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')
lat = 0
lon = 0
is_running = False

@socketio.on("connect")
def socket_connected():
    print("Socket Connected!")

@socketio.on("disconnect")
def socket_connected():
    print("Socket Disconnected!")

@app.route("/map", methods=["GET"])
def map():
    global lat, lon, is_running

    print("********************************* Is Running?? => ", is_running)
    if not is_running:
        try:
            is_running = True
            socketio.start_background_task(lambda: read_serial(socket=socketio))
        except Exception as e:
            is_running = False
            print(f"Failure on socket connect: {e}")
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5678, threaded=True)
