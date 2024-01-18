import serial, time

arduino = serial.Serial('COM3', 9600, timeout=1)
arduino.close()
arduino.open()

cards = [
    "aa bc da 81",
    "d9 c4 8d 9d",
]

while 1:
    txt = bytes(arduino.readline()).decode("utf-8").strip()
    if txt:
        print(txt)
        if txt in cards:
            print("Access Granted")
            arduino.write('1'.encode())
        else :
            print("Access Denied")
            # print(0)
    
    time.sleep(1)