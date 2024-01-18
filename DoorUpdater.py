import time, serial, json
from datetime import datetime, timedelta

users = {
    1: ["User 1", "aa bc da 81"],
    2: ["User 2", "d9 c4 8d 9d"],
}

arduino = serial.Serial('COM4', 9600, timeout=1)
arduino.close()
arduino.open()

with open("test.json") as jsonFile:
    doors = json.load(jsonFile)

times = {door : datetime.now() - timedelta(seconds=10) for door in doors.keys()}
# print(timer)
# exit()

while 1:
    txt = bytes(arduino.readline()).decode("utf-8").strip()
    try:
        if txt:
            print(txt)
            a, b = map(int, txt.split())
            # print(a, b)
            scanTime = datetime.now()
            doorId = a
            user = users[b][0]
            cardId = users[b][1]
            f = f"{scanTime.strftime("%Y-%m-%d %H:%M:%S")},{doorId},{cardId},{user}"
            with open("DoorLogs.csv", "a+") as logFile:
                logFile.write(f + '\n')
            times[f"door{a}"] = scanTime

    except:
        pass
    with open("test.json", "w+") as jsonFile:
        for door in doors:
            doors[door] = int((datetime.now() - times[door]).total_seconds() <= 10)

        jsonFile.write(json.dumps(doors, indent=4))
    # for door in doors:
    #     doors[door] = ((datetime.now() - t[door]).total_seconds() >= 5)
    # print(doors)

    time.sleep(.5)