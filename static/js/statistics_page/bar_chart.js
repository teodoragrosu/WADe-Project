function generate_bar_chart(bar_data) {
    var bar;
    if(bar_data) {
        bar = JSON.parse(bar_data);
    }
    else {
        bar = {avg_confirmed_per_day: 0, avg_deceased_per_day: 0, avg_recovered_per_day: 0 };
    }
    Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#292b2c';
    window.chartColors = {
          red: 'rgb(255, 99, 132)',
          orange: 'rgb(255, 159, 64)',
          yellow: 'rgb(255, 205, 86)',
          green: 'rgb(75, 192, 192)',
          blue: 'rgb(54, 162, 235)',
          purple: 'rgb(153, 102, 255)',
          grey: 'rgb(201, 203, 207)'
        };

    // define the chart data
    var barChartData = {
      labels : ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
      datasets : [
      {
          label: "deceased",
          backgroundColor: chartColors.red,
          borderColor: chartColors.red,
          data : Object.values(bar).map(function (value) { return parseFloat(value.avg_deceased_per_day).toFixed(2);}),
      },
      {
          label: "confirmed",
          lineTension: 0.1,
          backgroundColor: chartColors.orange,
          borderColor: chartColors.orange,
          data : Object.values(bar).map(function (value) { return parseFloat(value.avg_confirmed_per_day).toFixed(2);}),
      },
      {
          label: "recovered",
          backgroundColor: chartColors.green,
          borderColor: chartColors.green,
          data : Object.values(bar).map(function (value) { return parseFloat(value.avg_recovered_per_day).toFixed(2);}),
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
var bar;
    if(bar_results) {
        bar = JSON.parse(bar_results);
        myBarChart.data.datasets = [
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
          }
          ]
    }
    else {
        myBarChart.data.datasets = [
              {
                  label: "deceased",
                  backgroundColor: chartColors.red,
                  borderColor: chartColors.red,
                  data : [0],
              },
              {
                  label: "confirmed",
                  lineTension: 0.1,
                  backgroundColor: chartColors.orange,
                  borderColor: chartColors.orange,
                  data : [0],
              },
              {
                  label: "recovered",
                  backgroundColor: chartColors.green,
                  borderColor: chartColors.green,
                  data : [0],
              }
          ]
    }
    myBarChart.update();
}