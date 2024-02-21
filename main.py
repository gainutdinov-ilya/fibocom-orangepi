from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import dhcp
import sys_utils
import json
import starlette
import fibocom_utils
import threading
import web_helpers

MODEM_STATUS = 0

app = FastAPI()

container = {
    "timestamps": [],
    "signal": [],
    "temp": [],
    "cpu_temp": [],
    "metric_rspr": [],
    "metric_rsrq": [],
    "metric_rssnr": [],
    "metric_imbal": [],
}

metrics_thread = threading.Thread(target=web_helpers.webInfo, args=[container], daemon=True)
metrics_thread.start()

app.mount("/static" , StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates/")

@app.get("/")
async def index(request: Request):
    leases = dhcp.get_dhcp_lease_list()
    context = {
        "leases": leases,
        "temp_cpu": sys_utils.get_cpu_temp(),
        "temp_modem": fibocom_utils.get_modem_temp(),
        "signal_strenth": fibocom_utils.get_signal_strength()
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)

@app.get("/api/dhcp.json")
async def get_dhcp_lease_list_json(request: Request):
    leases = dhcp.get_dhcp_lease_list()
    return JSONResponse(content=leases)

@app.websocket("/ws")
async def websoket_handler(websocket: WebSocket):
    global container
    try:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            parsed_data = json.loads(data)
            if  parsed_data["method"] == "cpu_temp":
                cpu_temp = sys_utils.get_cpu_temp()
                response = {"type": parsed_data["method"], "data": cpu_temp}
                await websocket.send_text(json.dumps(response))
            elif  parsed_data["method"] == "dhcp_list":
                dhcp_list = dhcp.get_dhcp_lease_list()
                response = {"type": parsed_data['method'], "data": dhcp_list}
                await  websocket.send_text(json.dumps(response))
            elif  parsed_data["method"] == "get_ip":
                ip = fibocom_utils.ip
                response = {"type": parsed_data['method'], "data": ip}
                await  websocket.send_text(json.dumps(response))
            elif  parsed_data["method"] == "modem_temp":
                temp = fibocom_utils.get_modem_temp()
                response = {"type": parsed_data['method'], "data": temp}
                await  websocket.send_text(json.dumps(response))
            elif  parsed_data["method"] == "get_metrics":
                response = {"type": parsed_data['method'], "data": container}
                await websocket.send_text(json.dumps(response))

    except starlette.websockets.WebSocketDisconnect:
        return
