function generate_totals_chart(totals_data) {
    var totals;
    var upper_threshold = 1000;

    if(totals_data){
        totals = JSON.parse(totals_data);

        var maxOfList = Math.max(...Object.values(totals));
        var zeroes = maxOfList.toString().length-1;
        upper_threshold = Math.ceil(maxOfList / Math.pow(10, zeroes)) * Math.pow(10, zeroes);
    }
    else{
        var dayList = getDaysArray(new Date("2020-01-01"),new Date());

        (arr = []).length =  dayList.length;
         arr.fill(0);
        totals = {"line_labels": dayList,"line_values": arr};
    }

    // define the chart data
    var totalsChartData = {
      labels : Object.keys(totals),
      datasets : [{
            backgroundColor: "rgb(255, 99, 132)",
            borderColor: "rgb(255, 99, 132)",
            borderCapStyle: 'butt',
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            barPercentage: 0.5,
            barThickness: 10,
            maxBarThickness: 8,
            minBarLength: 2,
            data: Object.values(totals),
            spanGaps: false
      }]
    }

    // get chart canvas
    var ctx = document.getElementById("totalsChart").getContext("2d");

    // create the chart using the chart canvas
    myTotalsChart = new Chart(ctx, {
      type: 'bar',
      data: totalsChartData,
      options: {
          legend: {
            display: false
        },
        responsive: true,
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
                stacked: true,
                gridLines: {
                  display: false
                }
            }],
            yAxes: [{
                ticks: {
                  min: 0,
                  maxTicksLimit: 5
                },
                gridLines: {
                  color: "rgba(0, 0, 0, .125)",
                }
              }],
        }}
    });
};