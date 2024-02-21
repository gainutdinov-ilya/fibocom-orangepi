const ctxModemTemp = document.getElementById('ModemTemp');

var ModemTempChart = new Chart(ctxModemTemp, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Температура Модема',
            data: [],
            fill: false,
            borderColor: 'rgb(255, 0, 0)',
            tension: 0.1,
        },
        {
            label: 'Температура OrangePI',
            data: [],
            fill: false,
            borderColor: 'rgb(255,127,80)',
            tension: 0.1,
        }
    ]
    },
    options: {
        scales:{
            x: {
                maxTicksLimit: 60,
            }
        },
        animation: {
            duration: 0
        }
    }
});

function updateTempChart(temp_modem_values, temp_cpu_values, timestamps) {
    temp_modem_values = temp_modem_values.map(function (value) {
        return Number.parseInt(value);
    });
    temp_cpu_values = temp_cpu_values.map(function (value) {
        return Number.parseInt(value);
    });
    ModemTempChart.data.datasets[0].data = temp_modem_values;
    ModemTempChart.data.datasets[1].data = temp_cpu_values;
    ModemTempChart.data.labels = timestamps;
    ModemTempChart.update();
}





