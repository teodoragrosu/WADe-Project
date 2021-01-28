window.chartColors = {
  red: 'rgb(255, 99, 132)',
  orange: 'rgb(255, 159, 64)',
  yellow: 'rgb(255, 205, 86)',
  green: 'rgb(75, 192, 192)',
  blue: 'rgb(54, 162, 235)',
  purple: 'rgb(153, 102, 255)',
  grey: 'rgb(201, 203, 207)',
};

class PieChart {
  constructor() {
    this.data = {
      pie_labels: ['Total confirmed', 'Total recovered', 'Total deceased'],
      pie_values: ['0', '0', '0'],
    };

    this.chart = null;
  }

  initilize(data) {
    this.extractData(data);
    this.generateChart();
  }

  update(data) {
    if (!this.chart) {
      this.initilize(data);

      return;
    }

    this.extractData(data);

    this.chart.data.labels = this.data.pie_labels;
    this.chart.data.datasets[0].data = this.data.pie_values;
    this.chart.update();
  }

  extractData(data) {
    if (!data) {
      this.data = {
        pie_labels: ['Total confirmed', 'Total recovered', 'Total deceased'],
        pie_values: ['0', '0', '0'],
      };

      return;
    }

    this.data = {
      pie_labels: ['Total confirmed', 'Total recovered', 'Total deceased'],
      pie_values: [
        data.total_confirmed,
        data.total_recovered,
        data.total_deceased,
      ],
    };
  }

  generateChart() {
    const pieChartData = {
      labels: this.data.pie_labels,
      datasets: [{
        data: this.data.pie_values,
        backgroundColor: [
          window.chartColors.green,
          window.chartColors.orange,
          window.chartColors.red,
        ],
      }],
    };

    const chartNode = document.getElementById('pieChart').getContext('2d');

    this.chart = new window.Chart(chartNode, {
      type: 'pie',
      data: pieChartData,
      options: {
        responsive: true,
        tooltips: {
          callbacks: {
            label(tooltipItem, data) {
              const value = data.datasets[0].data[tooltipItem.index];

              return value.toString().split(/(?=(?:...)*$)/).join(',');
            },
          },
        },
      },
    });
  }
}

window.pieChart = new PieChart();