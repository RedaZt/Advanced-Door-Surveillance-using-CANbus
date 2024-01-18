import uvicorn, json, datetime
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# uvicorn app:app --reload

app = FastAPI()
# print(Path(__file__).parent.absolute() / "static")
app.mount(
    "/assests",
    StaticFiles(directory=Path(__file__).parent.absolute() / "assests"),
    name="assests",
)

templates = Jinja2Templates(directory="templates")


async def f():
    data = {}
    with open("test.json") as jsonFile:
        data = json.load(jsonFile)
    return data

async def f2():
    d = []
    with open("DoorLogs.csv") as csvFile:
        for line in csvFile:
            # print(line)
            d += line,
    # for i in range(50):
    #     d += s,
    return {"logs": d}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    states = ["Closed", "Open"]

    message = "Doors Test"

    now = datetime.now() 
    current_time = now.strftime("%Y-%m-%d %H:%M:%S") 

    with open("test.json") as jsonFile:
        d = json.load(jsonFile)
        status = [states[i] for i in d.values()]
        jsonFile.close()

    # s = "00:00,Reda Zitouni"

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "message": message,
            "current_time": current_time,
            "status": status,
        }
)

@app.get("/test")
async def get_data_route():
    return await f()

@app.get("/doorlogs")
async def get_data_route():
    return await f2()