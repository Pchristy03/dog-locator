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
            lat = line.find(b"lat: ")
            lon = line.find(b"lon: ")

            if lat != -1 and lon != -1:
                lon_val = line[lon+5:lon+15]
                lat_val = line[lat+5:lat+14]

                location = {lat: lat_val, lon: lon_val}
                socket.emit("serial", json.dumps(location))
            else:
                print(f"Invalid Lat and Lon: {lat}, {lon}")
        else:
            print("Line had no value from serial")

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