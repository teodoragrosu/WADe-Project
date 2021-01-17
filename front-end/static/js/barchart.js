Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// define the chart data
var barChartData = {
  labels : ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
  datasets : [
  {
      label: "deceased",
      backgroundColor: chartColors.red,
      borderColor: chartColors.red,
      data : window.bar_chart_data.data.map(({avg_deceased_per_day}) => avg_deceased_per_day),
  },
  {
      label: "confirmed",
      lineTension: 0.1,
      backgroundColor: chartColors.orange,
      borderColor: chartColors.orange,
      data : window.bar_chart_data.data.map(({avg_confirmed_per_day}) => avg_confirmed_per_day),
  },
  {
      label: "recovered",
      backgroundColor: chartColors.green,
      borderColor: chartColors.green,
      data : window.bar_chart_data.data.map(({avg_recovered_per_day}) => avg_recovered_per_day),
  }]
}

// get chart canvas
var ctx = document.getElementById("barChart").getContext("2d");

// create the chart using the chart canvas
var barChart = new Chart(ctx, {
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
