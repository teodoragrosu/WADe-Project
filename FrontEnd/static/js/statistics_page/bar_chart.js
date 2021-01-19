function generate_bar_chart(bar_data) {
    var bar = JSON.parse(bar_data);
    console.log(bar);
    Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#292b2c';

    console.log(Object.keys(bar).map(function (key) { return key.avg_deceased_per_day;}))
    // define the chart data
    var barChartData = {
      labels : ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
      datasets : [
      {
          label: "deceased",
          backgroundColor: chartColors.red,
          borderColor: chartColors.red,
          data : Object.values(bar).map(function (value) { return value.avg_deceased_per_day;}),
      },
      {
          label: "confirmed",
          lineTension: 0.1,
          backgroundColor: chartColors.orange,
          borderColor: chartColors.orange,
          data : Object.values(bar).map(function (value) { return value.avg_confirmed_per_day;}),
      },
      {
          label: "recovered",
          backgroundColor: chartColors.green,
          borderColor: chartColors.green,
          data : Object.values(bar).map(function (value) { return value.avg_recovered_per_day;}),
      },
      {
          label: "active",
          backgroundColor: chartColors.purple,
          borderColor: chartColors.blue,
          data : Object.values(bar).map(function (value) { return value.avg_active_per_day;}),
      }
      ]
    }

    // get chart canvas
    var ctx = document.getElementById("barChart").getContext("2d");

    // create the chart using the chart canvas
    myBarChart = new Chart(ctx, {
      type: 'bar',
      data: barChartData,
      options: {
        responsive: true,
        legend: {
            position: 'top',
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        scales: {
            xAxes: [{
                stacked: true
            }],
            yAxes: [{
                stacked: true
            }]
        }}
    });
}

function update_bar(bar_results){
    var bar = JSON.parse(bar_results);
    myBarChart.data.datasets[0].data = bar.bar_values;
    myBarChart.update();
}