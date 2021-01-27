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
    var pie;
    if(pie_results) {
        pie = JSON.parse(pie_results);
        var pie_data = {"pie_labels": ["Total confirmed", "Total recovered", "Total deceased"], "pie_values": [Object.entries(pie)[0][1]["total_confirmed"],Object.entries(pie)[0][1]["total_recovered"], Object.entries(pie)[0][1]["total_deceased"]]};
        myPieChart.data.labels = pie_data.pie_labels;
        myPieChart.data.datasets[0].data = pie_data.pie_values;
    }
    else {
        pie = {"pie_labels": ["Total confirmed", "Total recovered", "Total deceased"], "pie_values": ["0", "0", "0"]}
        myPieChart.data.labels = pie.pie_labels;
        myPieChart.data.datasets[0].data = pie.pie_values;
    }
    myPieChart.update();
}