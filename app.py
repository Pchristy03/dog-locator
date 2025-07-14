from map_processor import get_coord_pixel_location
import cv2
from flask import Flask, render_template
from flask_socketio import SocketIO
import json

from serial_reader import read_serial, simulate_info

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')
lat = 0
lon = 0
is_running = False

def main(coords):
    map = cv2.imread("somerset.png")
    print("Coords: ", coords)
    #40.78647490131012, -96.60745776292396
    pic_location = get_coord_pixel_location(coords[0], coords[1])
    print("Pic locations: ", pic_location)
    cv2.imwrite("static/map_copy.png", map)

    map_copy = cv2.imread("static/map_copy.png")
    cv2.circle(map_copy, pic_location, 5, (0, 255, 0), 2)
    cv2.imwrite("static/map_copy.png", map_copy)

@socketio.on("connect")
def socket_connected():
    print("Socket Connected!")


@socketio.on("updated_data")
def updated_data(json_d):
    global lat
    global lon

    print("json_d: ", json_d)
    json_d = json.loads(json_d)

    lat = json_d["lat"]
    lon = json_d["lon"]
    main((lat, lon))


@socketio.on("disconnect")
def socket_connected():
    print("Socket Disconnected!")

@app.route("/map", methods=["GET"])
def map():
    global lat, lon, is_running

    print("Is Running?? => ", is_running)
    if not is_running:
        try:
            is_running = True
            print("Is Running?? => ", is_running)
            socketio.start_background_task(lambda: read_serial(socket=socketio))
        except Exception as e:
            is_running = False
            print("Is Running?? => ", is_running)
            print(f"Failure on socket connect: {e}")
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5678, threaded=True)
