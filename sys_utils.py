import math
import subprocess

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

if __name__ == "__main__":
    print(get_cpu_temp())