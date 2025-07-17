import serial
import time
import json
import random

from map_processor import update_image



def read_serial(socket):
    received_data = False
    no_data_count = 0
    print("Creating Serial Port")
    ser = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1)
    time.sleep(2)

    ser.reset_input_buffer()
    ser.flush()

    time.sleep(3)
    print("Flushed Serial")

    while True:
        received_data = False

        if (no_data_count > 3):
            no_data_count = 0
            socket.emit("has_data", {"has_data": False, "lost_connection": True})

        line = ser.readline().decode().strip()
        ser.flush()

        if len(line) != 0:
            try:
                open_b = line.index("{")
                closed_b = line.index("}") + 1
                data = json.loads(line[open_b:closed_b])

                if "lat" in data and "lon" in data:
                    received_data = True
                    lat_val = data["lat"]
                    lon_val = data["lon"]

                    if lat_val and lon_val:
                        location = {"lat": float(lat_val), "lon": float(lon_val)}
                        socket.emit("serial", json.dumps(location))
                        socket.emit("has_data", {"has_data": True, "lost_connection": False})
                        update_image((float(lat_val), float(lon_val)))
                        socket.emit("updated_image", location)
                        no_data_count = 0
                    else:
                        print(f"Invalid Lat and Lon: {lat_val}, {lon_val}")

                if "info" in data:
                    received_data = True

            except Exception as e:
                print(f"Failed to parse location: {e}")
        else:
            print("Line had no value from serial")
            
        time.sleep(3)
    
        if not received_data:
            no_data_count = no_data_count + 1

def simulate_info():
    while True:
        lat = random.uniform(40.786, 40.787)
        lon = random.uniform(-96.60745779,-96.6070000)   

        data = json.dumps({
            "lat": lat,
            "lon": lon,
        }) 
        update_image(data)

        time.sleep(4)
