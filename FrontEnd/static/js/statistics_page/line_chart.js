function generate_line_chart(line_data) {
    var line = JSON.parse(line_data);

    // define the chart data
    var lineChartData = {
      labels : line.line_labels,
      datasets : [{
          fill: true,
          lineTension: 0.1,
          backgroundColor: "rgba(75,192,192,0.4)",
          borderColor: "rgba(75,192,192,1)",
          borderCapStyle: 'butt',
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
          data : line.line_values,
          spanGaps: false
      }]
    }

    // get chart canvas
    var ctx = document.getElementById("lineChart").getContext("2d");
    var maxOfList = Math.max(...line.line_values);
    var zeroes = maxOfList.toString().length-1;
    var upper_threshold = Math.ceil(maxOfList / Math.pow(10, zeroes)) * Math.pow(10, zeroes);

    // create the chart using the chart canvas
    myLineChart = new Chart(ctx, {
      type: 'line',
      data: lineChartData,
      options: {
        scales: {
          xAxes: [{
            time: {
              unit: 'date'
            },
            gridLines: {
              display: false
            },
            ticks: {
              maxTicksLimit: 7
            }
          }],
          yAxes: [{
            ticks: {
              min: 0,
              max: upper_threshold,
              maxTicksLimit: 5
            },
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
};

function update_line(line_results){
    var line = JSON.parse(line_results);
    myLineChart.data.labels = line.line_labels
    myLineChart.data.datasets[0].data = line.line_values
    myLineChart.update();
}