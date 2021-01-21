function generate_pie_chart(pie_data) {
    var pie;

    if(pie_data) {
        pie = JSON.parse(pie_data);
    }
    else {
        pie = {"pie_labels": ["Total recovered", "Total confirmed", "Total deceased"], "pie_values": ["0", "0", "0"]}
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
      labels : pie.pie_labels,
      datasets : [{
        data : pie.pie_values,
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
            responsive: true
        }
    });
}

function update_pie(pie_results){
    var pie = JSON.parse(pie_results);
    myPieChart.data.labels = pie.pie_labels;
    myPieChart.data.datasets[0].data = pie.pie_values;
    myPieChart.update();
}