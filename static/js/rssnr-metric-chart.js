const ctxMetricRssnr = document.getElementById('MetricRssnr');

var MetricRssnrChart = new Chart(ctxMetricRssnr, {
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
        label: 'RSSNR '.concat(counter),
        data: [],
        fill: false,
        tension: 0.1,
    };
    MetricRssnrChart.data.datasets.push(dataset)
}

function updateMetricRssnrChart(temp_values, timestamps) {
    for(dataset of temp_values)
    {
        let chart_pointer = 0;
        for(let antenna_pointer = 0; antenna_pointer < dataset.length; antenna_pointer++)
        {
            let row = dataset[antenna_pointer];
            for(let pointer = 0; pointer < row.length; pointer++)
            {
                let num = Number.parseFloat(row[pointer]);
                MetricRssnrChart.data.datasets[chart_pointer].data.push(num);
                chart_pointer++;
            }
        }
    }
    MetricRssnrChart.data.labels = timestamps;
    MetricRssnrChart.update();
}



let countRssnr = 12;
for(let i = 0; i < countRssnr; i++)
{
    createDatasetRsrq(i);
}

