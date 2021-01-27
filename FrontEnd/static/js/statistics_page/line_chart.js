var getDaysArray = function(start, end) {
    for(var arr=[],dt=new Date(start); dt<=end; dt.setDate(dt.getDate()+1)){
        arr.push($.format.date(new Date(dt),'yyyy-MM-dd'));
    }
    return arr;
};

function generate_line_chart(line_data) {
    var line;
    var upper_threshold = 1000;

    if(line_data){
        line = JSON.parse(line_data);

        var maxOfList = Math.max(...Object.values(line));//line.line_values);
        var zeroes = maxOfList.toString().length-1;
        upper_threshold = Math.ceil(maxOfList / Math.pow(10, zeroes)) * Math.pow(10, zeroes);
    }
    else{
        var dayList = getDaysArray(new Date("2020-01-01"),new Date());

        (arr = []).length =  dayList.length;
         arr.fill(0);
        line = {"line_labels": dayList,"line_values": arr};
    }

    // define the chart data
    var lineChartData = {
      labels : Object.keys(line),
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
          data : Object.values(line),
          spanGaps: false
      }]
    }

    // get chart canvas
    var ctx = document.getElementById("lineChart").getContext("2d");

    // create the chart using the chart canvas
    myLineChart = new Chart(ctx, {
      type: 'line',
      data: lineChartData,
      options: {
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
        },
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
              maxTicksLimit: 5,
              userCallback: function(value, index, values) {
							// Convert the number to a string and splite the string every 3 charaters from the end
							value = value.toString();
							value = value.split(/(?=(?:...)*$)/);
							value = value.join(',');
							return value;
						}
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

function update_line(line_results, toReverse=1){
    if(line_results) {
        var values;
        var line = JSON.parse(line_results);
        var labels = Object.keys(line).sort();
        if(toReverse) {
            values = Object.values(line).map(a => a.active).reverse();
            }
        else {
            values = Object.values(line).map(a => a.active);
        }

        var maxOfList = Math.max(...values);
        var zeroes = maxOfList.toString().length-1;

        upper_threshold = Math.ceil(maxOfList / Math.pow(10, zeroes)) * Math.pow(10, zeroes);

        myLineChart.data.labels = labels;
        myLineChart.data.datasets[0].data = values;
        myLineChart.options.scales.yAxes[0].ticks.max = upper_threshold;
    }
    else {
        var dayList = getDaysArray(new Date("2020-01-01"),new Date());

        (arr = []).length =  dayList.length;
         arr.fill(0);

        myLineChart.data.labels = dayList;
        myLineChart.data.datasets[0].data = arr;
        myLineChart.options.scales.yAxes[0].ticks.max = 1000;
    }

    myLineChart.update();
}