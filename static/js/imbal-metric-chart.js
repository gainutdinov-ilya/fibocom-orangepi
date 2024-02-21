const ctxMetricImbal = document.getElementById('MetricImbal');

var MetricImbal= new Chart(ctxMetricImbal, {
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
        label: 'IMBAL '.concat(counter),
        data: [],
        fill: false,
        tension: 0.1,
    };
    MetricImbal.data.datasets.push(dataset)
}

function updateMetricImbalChart(temp_values, timestamps) {
    for(dataset of temp_values)
    {
        let chart_pointer = 0;
        for(let antenna_pointer = 0; antenna_pointer < dataset.length; antenna_pointer++)
        {
            let row = dataset[antenna_pointer];
            for(let pointer = 0; pointer < row.length; pointer++)
            {
                let num = Number.parseFloat(row[pointer]);
                if(num < -50)
                {
                    num = 0.0;
                }
                MetricImbal.data.datasets[chart_pointer].data.push(num);
                chart_pointer++;
            }
        }
    }
    MetricImbal.data.labels = timestamps;
    MetricImbal.update();
}



let countImbal = 6;
for(let i = 0; i < countImbal; i++)
{
    createDatasetRsrq(i);
}

