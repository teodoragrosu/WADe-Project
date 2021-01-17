Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// define the chart data
var lineChartData = {
  labels : window.line_chart_data.labels,
  datasets : [
  {
      fill: false,
      label: "confirmed",
      lineTension: 0.1,
      backgroundColor: chartColors.orange,
      borderColor: chartColors.orange,
      pointRadius: 1,
      pointHitRadius: 10,
      data : window.line_chart_data.data.confirmed,
      spanGaps: false
  },
  {
      fill: false,
      label: "deceased",
      lineTension: 0.1,
      backgroundColor: chartColors.red,
      borderColor: chartColors.red,
      pointRadius: 1,
      pointHitRadius: 10,
      data : window.line_chart_data.data.deceased,
      spanGaps: false
  },
  {
      fill: false,
      label: "recovered",
      lineTension: 0.1,
      backgroundColor: chartColors.green,
      borderColor: chartColors.green,
      pointRadius: 1,
      pointHitRadius: 10,
      data : window.line_chart_data.data.recovered,
      spanGaps: false
  }]
}

// get chart canvas
var ctx = document.getElementById("casesChart").getContext("2d");

// create the chart using the chart canvas
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: lineChartData,
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
