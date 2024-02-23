import math
import subprocess
import psutil
import time

def get_cpu_temp():
    tempPath = "/sys/devices/virtual/thermal/thermal_zone0/temp"
    temp = 0
    with open(tempPath, "r") as file:
        temp = file.read()
        file.close()
    temp = str(math.ceil(int(temp)))[0:2]
    return temp


def get_uptime_begins():
    process = subprocess.Popen(['uptime', '--parsable'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    process.wait()


def get_network_speed():
    net_io = psutil.net_io_counters()

    last_bytes_sent = psutil.net_io_counters().bytes_sent
    last_bytes_recv = psutil.net_io_counters().bytes_recv
    time.sleep(1)  # Ждем 1 секунду
    new_bytes_sent = psutil.net_io_counters().bytes_sent
    new_bytes_recv = psutil.net_io_counters().bytes_recv

    # Вычисляем скорость потребления сети в байтах в секунду
    download_speed = new_bytes_recv - last_bytes_recv
    upload_speed = new_bytes_sent - last_bytes_sent

    download_speed = download_speed / 1e6 * 8 
    upload_speed = upload_speed / 1e6 * 8 
    download_speed = "{:.2f}".format(download_speed)
    upload_speed = "{:.2f}".format(upload_speed)
    return [download_speed, upload_speed]

if __name__ == "__main__":
    print(get_cpu_temp())