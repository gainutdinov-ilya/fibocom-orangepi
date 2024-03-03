import os
import subprocess
from settings import *
import json
import re
import sys
import time
import socket
import datetime
import sys

def __debug_message(data):
    global debug
    time = datetime.datetime.now().ctime()
    if debug:
        print(f"{time} FibocomUtils: {data}")


def __invoke_modem_command(modem_number: int, command: str, wait = 1) -> str:
    global debug
    if True:
        print(f"Invoke command: {command} For modem: {modem_number}...", end="")
    process = subprocess.Popen(['mmcli', '-m', str(modem_number), f"--command={command}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(wait)
    stdout, stderr = process.communicate()
    process.wait()
    stdout = stdout.decode("UTF-8")
    stdout = stdout.replace('\n', '')
    if stdout.startswith("error"):
        if debug:
            print(f"FALL")
            print(f"Exec Result = {stdout}")
        return "e"
    else:
        if debug:
            print(f"OK")
            print(f"Exec Result = {stdout}")
        return stdout


def setup_connection() -> bool: 
    global commands, modem, debug, ip

    attempts = 0

    while modem == -1:
        get_connected_modem()
        time.sleep(3)
        attempts += 1
        if attempts == 5:
            __debug_message("Can't connect, modem not found")
            return False
        

    out = str()
    __debug_message("Try to connect...")
    for command in commands:
        out = __invoke_modem_command(modem, command)
        if out == "e":
            __debug_message("Connection Failed!")
            return False
    __debug_message("Connection Done")
    if debug:
        print("Parsing ip...", end="")
    re_parse_ips = r'"[0-9.]*"'
    re_parse_ip = r"(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})"
    parse_first_step = re.findall(re_parse_ips, out)
    if len(parse_first_step) == 0:
        if debug:
            print("FAILED")
        return False
    
    ips = re.findall(re_parse_ip, parse_first_step[0])
    if len(ips) == 0:
        if debug:
            print("FAILED")
        return False

    ip = ips[0]

    if debug:
        print(f"OK IP: {ip}")


    global bridge_interface, modem_interface
    subprocess.Popen(["systemctl", "restart", "isc-dhcp-server"]).wait()
    subprocess.Popen(["/opt/fibocom/script_helpers/setup_net", bridge_interface, modem_interface, ip]).wait()
    time.sleep(10)
    return True


def restart_modem() -> bool:
    __debug_message("Try to restart modem...")
    global modem
    attempts = 0
    while modem == -1:
        get_connected_modem()
        time.sleep(3)
        attempts += 1
        if attempts == 5 and modem == -1:
            __debug_message("RestartModem: Fail - modem not found")
            return False

    command = "AT+CFUN=15"
    r = __invoke_modem_command(modem, command)
    if r == 'e':
        __debug_message("Failed to restart Modem")
        return False
    __debug_message(r)
    __debug_message("Restarting modem. Please Wait")
    return True



def __invoke_bash_command(command) -> str:
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    process.wait()
    process_data = stdout.decode('UTF-8')
    return process_data


def get_connected_modem() -> int:
    global modem
    process_data = __invoke_bash_command(["mmcli", "-L", "-J"])
    __debug_message(f"GetConnectedModem mmcli return: {process_data}")
    try:
        mmcli_data = json.loads(process_data)
    except:
        return -1
    re_modem_number = r"[0-9]$"
    if len(mmcli_data['modem-list']) == 0:
        __debug_message("GetConnectedModemError: Modem not available")
        return -1; 
    for modemString in mmcli_data['modem-list']:
        re_find_result = re.findall(re_modem_number, modemString)
        if len(re_find_result) == 0:
            return -1
        else:
            modem = int(re_find_result[0])
    return modem

def get_modem_temp():
    global modem
    get_connected_modem()
    out = __invoke_modem_command(modem, "AT+MTSM=1", 1)
    re_rule = r"'[\s\d\w\D]*"
    result = re.findall(re_rule, out)
    if len(result) == 0:
        return -1
    
    temp = re.findall(r"[0-9]{2}", result.pop()).pop()
    return temp

def get_signal_strength():
    global modem
    get_connected_modem()
    out = __invoke_modem_command(modem, "AT+RSRP?", 0)
    re_match_numbers = r"[\d.]*,"
    parsed_numbers = re.findall(re_match_numbers, out)
    if len(parsed_numbers) < 3:
        return -130
    signal_strength = parsed_numbers[2]
    signal_strength = signal_strength.replace(",",'')
    signal_strength = f"-{signal_strength}"
    return signal_strength

def get_signal_metics():
    global modem
    get_connected_modem()
    out = __invoke_modem_command(modem, "AT@errc:pcell_scell_measurement_info()", 1)
    #out = out.replace('\n', '')
    re_parse_rspr = r"rsrp\[[-\d\.,]*\]"
    re_parse_rsrq = r"rsrq\[[-\d\.,]*\]"
    re_parse_rssnr = r"rssnr\[[-\d\.,]*\]"
    re_parse_imbal = r"imbal\[[-\d\.,]*\]"
    re_parse_numbers = r"[-\d.\d]+"
    raw_rspr = re.findall(re_parse_rspr, out)
    raw_rsrq = re.findall(re_parse_rsrq, out)
    raw_rssnr = re.findall(re_parse_rssnr, out)
    raw_imbal = re.findall(re_parse_imbal, out)
    rspr = []
    rsrq = []
    rssnr = []
    imbal = []
    for parsed_rspr in raw_rspr:
        rspr.append(re.findall(re_parse_numbers, parsed_rspr))
    for parsed_rsrq in raw_rsrq:
        rsrq.append(re.findall(re_parse_numbers, parsed_rsrq))
    for parsed_rssnr in raw_rssnr:
       rssnr.append(re.findall(re_parse_numbers, parsed_rssnr))
    for parsed_imbal in raw_imbal:
        imbal.append(re.findall(re_parse_numbers, parsed_imbal))
    struct = {
        'rspr': rspr,
        'rsrq': rsrq,
        'rssnr': rssnr,
        'imbal': imbal
    }
    return struct

def get_modem_info():
    global modem
    if modem == -1:
        get_connected_modem()
    info = __invoke_bash_command(["mmcli", "-m", str(modem), "-J"])
    return json.loads(info)

def __online():
    try:
        host = "8.8.8.8"
        port = 53
        timeout = 3
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        __debug_message("Online: YES")
        return True
    except socket.error as err: 
        __debug_message("Online: NO")
        return False

def __interface_with_ip():
    global modem_interface
    ip_addr = __invoke_bash_command(["ifconfig", modem_interface])
    re_parse_ip = r"inet [0-9.]+"
    find = re.findall(re_parse_ip, ip_addr)
    if len(find) == 0:
        return False
    else:
        return True


def __connection_watcher():
    global modem, debug, modem_interface
    while modem == -1:
        __debug_message("Wait Modem...")
        modem = get_connected_modem()
        time.sleep(3)
    if not __online():
        if __interface_with_ip():
            restart_modem()
        setup_connection()
    while __online():
        time.sleep(30)
    else:
        restart_modem()
        __connection_watcher()


def print_help():
    print("?")

if __name__ == "__main__":
    debug = True
    if len(sys.argv) <= 1:
        __connection_watcher()
    elif len(sys.argv) > 2:
        print_help()
    if sys.argv[1] == "--restart":
        restart_modem()
    else:
        print_help()