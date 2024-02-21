commands = [
    'AT+CFUN=1',
    'AT+CGPIAF=1,0,0,0',
    'AT+CREG=0'
    'AT+CEREG=0',
    'AT+CGATT=0',
    'AT+COPS=2',
    'AT+XCESQRC=1',
    'AT+XACT=2,,,0',
    'AT+CGDCONT=0,"IP"',
    'AT+CGDCONT=0',
    'AT+CGDCONT=1,"IP","internet"',
    'AT+XDATACHANNEL=1,1,"/USBCDC/0","/USBHS/NCM/0",2,1',
    'AT+XDNS=1,1',
    'AT+CGACT=1,1',
    'AT+COPS=0,0',
    'AT+CGATT=1',
    'AT+CGDATA="M-RAW_IP",1',
    'AT+CGATT?; +CSQ?',
    'AT+CGCONTRDP=1'
]
modem = -1
debug = False
ip = "Not Connected"

bridge_interface = "br0"
modem_interface = "enx000011121314"

timings_length = 30