const ctxMetricRsrq = document.getElementById('MetricRsrq');

var MetricRsrqChart = new Chart(ctxMetricRsrq, {
    type: 'line',
    data: {
        labels: [],
        datasets: []
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

function createDatasetRsrq(counter){
    let dataset = {
        label: 'RSRQ '.concat(counter),
        data: [],
        fill: false,
        tension: 0.1,
    };
    MetricRsrqChart.data.datasets.push(dataset)
}

function updateMetricRsrqChart(temp_values, timestamps) {
    for(dataset of temp_values)
    {
        let chart_pointer = 0;
        for(let antenna_pointer = 0; antenna_pointer < dataset.length; antenna_pointer++)
        {
            let row = dataset[antenna_pointer];
            for(let pointer = 0; pointer < row.length; pointer++)
            {
                let num = Number.parseFloat(row[pointer]);
                MetricRsrqChart.data.datasets[chart_pointer].data.push(num);
                chart_pointer++;
            }
        }
    }
    MetricRsrqChart.data.labels = timestamps;
    MetricRsrqChart.update();
}



let countRsrq = 12;
for(let i = 0; i < countRsrq; i++)
{
    createDatasetRsrq(i);
}

