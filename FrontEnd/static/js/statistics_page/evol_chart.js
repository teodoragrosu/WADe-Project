function generate_evol_chart(evol_data) {
    var evol;
    var upper_threshold = 1000;

    if(evol_data){
        evol = JSON.parse(evol_data);

        var maxOfList = Math.max(...evol.evol_recovered);
        var zeroes = maxOfList.toString().length-1;
        upper_threshold = Math.ceil(maxOfList / Math.pow(10, zeroes)) * Math.pow(10, zeroes);
    }
    else{
        var dayList = getDaysArray(new Date("2020-01-01"),new Date());

        (arr = []).length =  dayList.length;
         arr.fill(0);
        evol = {"evol_labels": dayList, "evol_recovered": arr, "evol_deceased": arr};
    }

    // define the chart data
    var evolChartData = {
      labels : evol.evol_labels,
      datasets : [{
        data: evol.evol_recovered,
        label: "Recovered",
        borderColor: "#3e95cd",
        fill: false
      }, {
        data: evol.evol_deceased,
        label: "Deceased",
        borderColor: "#8e5ea2",
        fill: false
      }]
    }

    // get chart canvas
    var ctx = document.getElementById("evolChart").getContext("2d");

    // create the chart using the chart canvas
    myEvolChart = new Chart(ctx, {
      type: 'line',
      data: evolChartData,
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
          }]
         }
        }
    });
}

function update_evol(evol_results){
    var evol = JSON.parse(evol_results);
    var maxOfList = Math.max(...evol.evol_recovered);
    var zeroes = maxOfList.toString().length-1;
    var upper_threshold = Math.ceil(maxOfList / Math.pow(10, zeroes)) * Math.pow(10, zeroes);
    myEvolChart.data.labels = evol.evol_labels;
    myEvolChart.data.datasets[0].data = evol.evol_recovered;
    myEvolChart.data.datasets[1].data = evol.evol_deceased;
    myEvolChart.options.scales.yAxes[0].ticks.max = upper_threshold;
    myEvolChart.update();
}