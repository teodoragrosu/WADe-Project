var pieChartData = {
  labels : window.pie_chart_data.labels,
  datasets : [{
    data : window.pie_chart_data.data,
    backgroundColor: [
        window.chartColors.green,
        window.chartColors.orange,
        window.chartColors.red,
    ],
  }]
}

var pie = document.getElementById("pieChart").getContext("2d");

var myPieChart = new Chart(pie, {
    type: 'pie',
    data: pieChartData,
    options: {
        responsive: true
    }
});
