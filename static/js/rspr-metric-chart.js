const ctxMetricRspr = document.getElementById('MetricRspr');

var MetricRsprChart = new Chart(ctxMetricRspr, {
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

function createDatasetRspr(counter){
    let dataset = {
        label: 'RSPR '.concat(counter + 1),
        data: [],
        fill: false,
        tension: 0.1,
    };
    MetricRsprChart.data.datasets.push(dataset)
}

function updateMetricRsprChart(temp_values, timestamps) {
    for(dataset of temp_values)
    {
        let chart_pointer = 0;
        for(let antenna_pointer = 0; antenna_pointer < dataset.length; antenna_pointer++)
        {
            let row = dataset[antenna_pointer];
            for(let pointer = 0; pointer < row.length; pointer++)
            {
                let num = Number.parseFloat(row[pointer]);
                MetricRsprChart.data.datasets[chart_pointer].data.push(num);
                chart_pointer++;
            }
        }
    }
    MetricRsprChart.data.labels = timestamps;
    MetricRsprChart.update();
}



let countRspr = 12;
for(let i = 0; i < countRspr; i++)
{
    createDatasetRspr(i);
}

