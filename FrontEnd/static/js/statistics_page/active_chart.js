function generate_active_chart(active_data) {
    var active = JSON.parse(active_data);
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// define the chart data
var activeChartData = {
  labels : active.pie_labels,
  datasets : [
  {
      fill: true,
      labal: "active",
      lineTension: 0.1,
      backgroundColor: "rgba(75,192,192,0.4)",
      borderColor: "rgba(75,192,192,1)",
      borderCapStyle: 'butt',
      borderDash: [],
      borderDashOffset: 0.0,
      borderJoinStyle: 'miter',
      pointBorderColor: "rgba(75,192,192,1)",
      pointBackgroundColor: "#fff",
      pointBorderWidth: 1,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(75,192,192,1)",
      pointHoverBorderColor: "rgba(220,220,220,1)",
      pointHoverBorderWidth: 2,
      pointRadius: 1,
      pointHitRadius: 10,
      pointRadius: 1,
      pointHitRadius: 10,
      data : active.pie_values,
      spanGaps: false
  }]
}

    // get chart canvas
    var ctx = document.getElementById("activeChart").getContext("2d");

    // create the chart using the chart canvas
    var activeChart = new Chart(ctx, {
      type: 'line',
      data: activeChartData,
      options: {
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
            time: {
              unit: 'date'
            },
            gridLines: {
              display: false
            }
          }],
          yAxes: [{
            gridLines: {
              color: "rgba(0, 0, 0, .125)",
            }
          }],
        },
        legend: {
          display: false
        }
      }
    });
}

function update_active(active_results){
    var active = JSON.parse(active_results);
    myActiveChart.data.labels = active.pie_labels;
    myActiveChart.data.datasets[0].data = active.pie_values;
    myActiveChart.update();
}