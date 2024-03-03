import threading
import fibocom_utils
from settings import *
import time
import datetime
import sys_utils
from oled_thread import *

debug = False


container_test = {
    "timestamps": [],
    "signal": [],
    "temp": [],
    "cpu_temp": [],
    "metric_rspr": [],
    "metric_rsrq": [],
    "metric_rssnr": [],
    "metric_imbal": [],
}



def __logger(message):
    time = datetime.datetime.now().isoformat()
    print(f"{time} WebinfoHelpers: {message}")

def webInfo(container, aoh):
    __logger("Started")
    aoh.addText("CPU: ?")
    aoh.addText("MODEM: ?")
    aoh.addText("SIGNAL: ?")
    aoh.addText("CONNECT: ?")
    aoh.addText("DOWN: ?")
    aoh.addText("UP: ?")
    global timings, timings_length, modem, debug
    debug = True
    update_time = 0.2
    while True:
        if modem == -1:
            __logger("Wait modem...")
            time.sleep(update_time)
            modem = fibocom_utils.get_connected_modem()
            continue

        if len(container['timestamps']) >= timings_length:
            container['timestamps'].pop(0)
            container['signal'].pop(0)
            container['temp'].pop(0)
            container['cpu_temp'].pop(0)
            container['metric_rspr'].pop(0)
            container['metric_rsrq'].pop(0)
            container['metric_rssnr'].pop(0)
            container['metric_imbal'].pop(0)

        temp = fibocom_utils.get_modem_temp()
        signal_strength = fibocom_utils.get_signal_strength()
        container['timestamps'].append(datetime.datetime.now().time().strftime("%H:%M:%S"))
        container['temp'].append(temp)
        container['signal'].append(signal_strength)
        container['cpu_temp'].append(sys_utils.get_cpu_temp())
        metrics = fibocom_utils.get_signal_metics()
        container['metric_rspr'].append(metrics['rspr'])
        container['metric_rsrq'].append(metrics['rsrq'])
        container['metric_rssnr'].append(metrics['rssnr'])
        container['metric_imbal'].append(metrics['imbal'])
        __logger("Info Succesfully updated!")


        bw = sys_utils.get_network_speed()
        online = fibocom_utils.__online()
        if not online:
            online = "FAIL"
        else:
            online = "OK"
        aoh.editText(f"Cpu: {sys_utils.get_cpu_temp()}", 0)
        aoh.editText(f"Modem: {temp}", 1)
        aoh.editText(f"SIG: {signal_strength}", 2)
        aoh.editText(f"INET: {online}", 3)
        aoh.editText(f"DOWN: {bw[0]}", 4)
        aoh.editText(f"UP: {bw[1]}", 5)
        time.sleep(update_time)
  
  

if __name__ == "__main__":
    webInfo(container_test)