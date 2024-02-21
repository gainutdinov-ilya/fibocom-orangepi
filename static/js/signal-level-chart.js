const ctxSignal = document.getElementById('SignalInfo');

var SignalChart = new Chart(ctxSignal, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Уровень сигнала',
            data: [],
            fill: false,
            borderColor: 'green',
            tension: 0.1,
        }]
    },
    options: {
        scales: {
            x: {
                maxTicksLimit: 60,
            }
        },
        animation: {
            duration: 0
        }
    }
});

function updateSignalChart(temp_values, timestamps) {
    temp_values = temp_values.map(function (value) {
        return Number.parseFloat(value);
    });
    SignalChart.data.datasets[0].data = temp_values;
    SignalChart.data.labels = timestamps;
    SignalChart.update();
}





