import serial
import time
import json
import random

def read_serial(socket):
    print("Creating Serial Port")
    ser = serial.Serial("/dev/serial0", baudrate=115200, timeout=1)
    time.sleep(2)

    ser.reset_input_buffer()
    ser.flush()

    time.sleep(3)
    print("Flushed Serial")

    while True:
        line = ser.readline().decode().strip()
        ser.flush()

        if len(line) != 0:
            print(line)
            try:
                open_b = line.index("{")
                closed_b = line.index("}") + 1
                j = line[open_b:closed_b]
                print("j: ", j)
                data = json.loads(j)
                lat_val = data["lat"]
                lon_val = data["lon"]

                print("Lat and long: ", lat_val, lon_val)
                if lat_val != -1 and lon_val != -1:
                    # lon_val = line[lon+5:lon+15]
                    # lat_val = line[lat+5:lat+14]

                    location = {"lat": float(lat_val), "lon": float(lon_val)}
                    socket.emit("serial", json.dumps(location))
                else:
                    print(f"Invalid Lat and Lon: {lat_val}, {lon_val}")
            except Exception as e:
                print("Failed to parse location: {e}")
        else:
            print("Line had no value from serial")
            
        time.sleep(3)

def simulate_info(socket):
    while True:
        lat = random.uniform(40.786, 40.787)
        lon = random.uniform(-96.60745779,-96.6070000)   

        data = json.dumps({
            "lat": lat,
            "lon": lon,
        }) 

        socket.emit("serial", data)

        time.sleep(2)
