var ws = new WebSocket("ws://".concat(document.location.host).concat("/ws"));

ws.onmessage = function(event) {
    let data = JSON.parse(event.data);
    switch(data.type)
    {
        case "dhcp_list":
            updateDhcpList(data.data)
            break;
        case "get_metrics":
            updateCpuTemp(data.data['cpu_temp'][data.data['cpu_temp'].length - 1])
            updateModemTemp(data.data['temp'][data.data['temp'].length - 1])
            updateSignalStrenth(data.data['signal'][data.data['signal'].length - 1])
            updateTempChart(data.data['temp'], data.data['cpu_temp'], data.data['timestamps']);
            updateSignalChart(data.data['signal'], data.data['timestamps']);
            updateMetricRsprChart(data.data['metric_rspr'] ,data.data['timestamps']);
            updateMetricRsrqChart(data.data['metric_rsrq'] ,data.data['timestamps']);
            updateMetricRssnrChart(data.data['metric_rssnr'] ,data.data['timestamps']);
            updateMetricImbalChart(data.data['metric_imbal'] ,data.data['timestamps']);
            break;
    }
}

function callWsMethod(method)
{
    let data = {"method": method};
    if(ws.readyState == WebSocket.CLOSED)
    {
        return;
    }
    ws.send(JSON.stringify(data));
}

function updateCpuTemp(cpuTemp)
{
    document.getElementById("cputemp").innerHTML = "# Температура процессора: ".concat(cpuTemp);
}


function updateModemTemp(modemTemp)
{
    document.getElementById("modemtemp").innerHTML = "# Температура модема: ".concat(modemTemp);
}

function updateSignalStrenth(signalstrenth)
{
    document.getElementById("signalstrength").innerHTML = "# Уровень сигнала: ".concat(signalstrenth);
}


function updateDhcpList(dhcpList)
{
    var dhcpListEl = document.getElementById("dhcplist");
    dhcpListEl.innerText = "";
    for(let val of dhcpList)
    {
        let tr = document.createElement("tr");
        let tdMAC = document.createElement("td");
        tdMAC.innerText = val["MAC"];
        tr.appendChild(tdMAC);

        let tdHOSTNAME = document.createElement("td");
        tdHOSTNAME.innerText = val["HOSTNAME"];
        tr.appendChild(tdHOSTNAME);

        let tdIP = document.createElement("td");
        tdIP.innerText = val["IP"];
        tr.appendChild(tdIP);

        let tdSTART = document.createElement("td");
        tdSTART.innerText = val["START"];
        tr.appendChild(tdSTART);

        let tdEND = document.createElement("td");
        tdEND.innerText = val["END"];
        tr.appendChild(tdEND);

        dhcpListEl.appendChild(tr);
    }
}

setInterval(() => {
    callWsMethod("dhcp_list");
}, 5000);

setInterval(() => {
    callWsMethod("get_metrics");
}, 3000);

