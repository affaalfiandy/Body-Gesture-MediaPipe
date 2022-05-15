# Importing Libraries
import serial
import time

arduino = serial.Serial(port='COM6', baudrate=115200, timeout=0.1)
def write_read(x):
    x = str(x)
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline().decode('utf-8').rstrip()
    return data