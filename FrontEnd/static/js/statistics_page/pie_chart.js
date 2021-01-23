function generate_pie_chart(pie_data) {
    var pie;

    if(pie_data) {
        pie = JSON.parse(pie_data);
    }
    else {
        pie = {"pie_labels": ["Total confirmed", "Total recovered", "Total deceased"], "pie_values": ["0", "0", "0"]}
    }

    window.chartColors = {
          red: 'rgb(255, 99, 132)',
          orange: 'rgb(255, 159, 64)',
          yellow: 'rgb(255, 205, 86)',
          green: 'rgb(75, 192, 192)',
          blue: 'rgb(54, 162, 235)',
          purple: 'rgb(153, 102, 255)',
          grey: 'rgb(201, 203, 207)'
        };

    var pieChartData = {
      labels : Object.keys(pie),
      datasets : [{
        data : Object.values(pie),
        backgroundColor: [
            window.chartColors.green,
            window.chartColors.orange,
            window.chartColors.red,
        ],
      }]
    }

    var pie = document.getElementById("pieChart").getContext("2d");

    myPieChart = new Chart(pie, {
        type: 'pie',
        data: pieChartData,
        options: {
            responsive: true,
            tooltips: {
            callbacks: {
					label: function(tooltipItem, data) {
						var value = data.datasets[0].data[tooltipItem.index];
						value = value.toString();
						value = value.split(/(?=(?:...)*$)/);
						value = value.join(',');
						return value;
					}
			    }
            }
        }
    });
}

function update_pie(pie_results){
    var pie = JSON.parse(pie_results);
    myPieChart.data.labels = Object.keys(pie);
    myPieChart.data.datasets[0].data = Object.values(pie);
    myPieChart.update();
}