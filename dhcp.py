import subprocess
import re



def parse_value(leaseString, reRule):
    reRuleGetValue = r"[a-zA-Z0-9:\-\.]*"
    tempTarget = re.findall(reRule, leaseString)[0]
    if len(tempTarget) == 0:
        return "ERROR PARCING"
    target = re.findall(reRuleGetValue, tempTarget)
    if len(target) < 2:
        return "ERROR PARCING"
    return target[2]


def parse_time_value(leaseString, reRule):
    reRuleGetValue = r"[0-9-]+ [0-9:]*"
    tempTarget = re.findall(reRule, leaseString)[0]
    if len(tempTarget) == 0:
        return "ERROR PARCING"
    target = re.findall(reRuleGetValue, tempTarget)
    if len(target) == 0:
        return "ERROR PARCING"
    return target[0]



def get_dhcp_lease_list():
    process = subprocess.Popen(['dhcp-lease-list', '--parsable'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    process.wait()
    reRule = r"^([a-zA-Z0-9:-]*.*)"
    parsedLines = re.findall(reRule, stdout.decode('UTF-8'), re.M)
    listResult = list()
    reMac = r"MAC [a-zA-Z0-9:\-\.]*"
    reIP = r"IP [a-zA-Z0-9:\-\.]*"
    reHostname = r"HOSTNAME [a-zA-Z0-9:\-\.]*"
    reBeginTime = r"BEGIN [a-zA-Z0-9:\-\.]* [0-9:]*"
    reEndTime = r"END [a-zA-Z0-9:\-\.]* [0-9:]*"
    for line in parsedLines:
        if len(line) == 0:
            continue
        resultRow = dict()
        resultRow['MAC'] = parse_value(line, reMac)
        resultRow['IP'] = parse_value(line, reIP)
        resultRow['HOSTNAME'] = parse_value(line, reHostname)
        resultRow['START'] = parse_time_value(line, reBeginTime)
        resultRow['END'] = parse_time_value(line, reEndTime)
        listResult.append(resultRow)
    return listResult


if __name__ == "__main__":
    print(get_dhcp_lease_list())
