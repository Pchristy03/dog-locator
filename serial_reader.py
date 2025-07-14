import serial
import time
import json
import random



def read_serial(socket):
    received_data = False
    no_data_count = 0
    print("Creating Serial Port")
    ser = serial.Serial("/dev/serial0", baudrate=115200, timeout=1)
    time.sleep(2)

    ser.reset_input_buffer()
    ser.flush()

    time.sleep(3)
    print("Flushed Serial")



    while True:
        received_data = False

        if (no_data_count > 3):
            no_data_count = 0
            socket.emit("has_data", {"lost_connection": True})

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

                if "lat" in data:
                    received_data = True
                    lat_val = data["lat"]
                    lon_val = data["lon"]

                    print("Lat and long: ", lat_val, lon_val)
                    if lat_val != -1 and lon_val != -1:

                        location = {"lat": float(lat_val), "lon": float(lon_val)}
                        socket.emit("serial", json.dumps(location))
                        print("Emitting has_data:", {"has_data": True})
                        socket.emit("has_data", {"has_data": True})
                    else:
                        print(f"Invalid Lat and Lon: {lat_val}, {lon_val}")

                if "info" in data:
                    received_data = True
                    socket.emit("serial", json.dumps(data))

            except Exception as e:
                print(f"Failed to parse location: {e}")
        else:
            print("Line had no value from serial")
            
        time.sleep(3)
    
        if not received_data:
            no_data_count = no_data_count + 1
            socket.emit("has_data", {"has_data": False})

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
