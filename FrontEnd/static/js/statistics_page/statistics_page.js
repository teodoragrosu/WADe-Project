const apiPath = 'https://coda-apiv1.herokuapp.com/api';
// var apiPath = 'http://127.0.0.1:5000/api';
// var websitePath = 'http://localhost:8000/';

$.getScript('static/js/statistics_page/line_chart.js',
  () => {
    $.ajax({
      url: `${apiPath}/metrics/active`,
      type: 'GET',
      success: generate_line_chart,
    });
  });

async function updatePieChart() {
  let date = $('#pie_placeholder').datepicker('getDate');
  if (date) {
    date = $.format.date(new Date(date), 'yyyy-MM-dd');
  }
  const countryCode = $('#country-selector').val();
  if (countryCode !== 'Worldwide') {
    const url = new URL(`${apiPath}/country/${countryCode}`);
    if (date) {
      url.searchParams.set('date', date);
    }
    const response = await fetch(url.href);
    let data = await response.json();
    if (date) {
      data = data[date];
    } else {
      data = Object.entries(data)[0][1];
    }
    window.pieChart.update(data);
  } else {
    const url = new URL(`${apiPath}/metrics/pie`);
    if (date) {
      url.searchParams.set('date', date);
    }
    const response = await fetch(url.href);
    const data = await response.json();
    window.pieChart.update(data);
  }
}
$.getScript('static/js/statistics_page/pie_chart.js', updatePieChart);

$.getScript('static/js/statistics_page/bar_chart.js',
  () => {
    $.ajax({
      url: `${apiPath}/metrics/averages`,
      type: 'GET',
      success: generate_bar_chart,
    });
  });
$.getScript('static/js/statistics_page/evol_chart.js',
  () => {
    $.ajax({
      url: `${apiPath}/metrics/evols`,
      type: 'GET',
      success: generate_evol_chart,
      complete(data) {
        $('#mainLoader').addClass('invisible');
        $('#layoutSidenav_content').removeClass('invisible').addClass('visible');
      },
    });
  });
$.getScript('static/js/statistics_page/totals_chart.js',
  () => {
    $.ajax({
      url: `${apiPath}/metrics/totals`,
      type: 'GET',
      success: generate_totals_chart,
    });
  });

let myTotalsChart;
let myLineChart;
let myBarChart;
let myEvolChart;

$(() => {
  $('.date-box').datepicker({
    format: 'yyyy-mm-dd',
    startDate: '2020-01-01',
    endDate: '0',
  });
});

$('#country-selector').change(() => {
  $('.spinner-border').removeClass('invisible').addClass('visible');
  const countryCode = $('#country-selector').val();
  if (countryCode !== 'Worldwide') {
    $('#csv_button').prop('disabled', false);
    $('#json_button').prop('disabled', false);

    updatePieChart();

    $.ajax({
      url: `${apiPath}/country/${countryCode}`,
      type: 'get',
      dataType: 'html',
      success: update_line,
    });
    $.ajax({
      url: `${apiPath}/country/monthly/${countryCode}`,
      type: 'get',
      dataType: 'html',
      success: update_bar,
    });
    $.ajax({
      url: `${apiPath}/country/${countryCode}`,
      type: 'get',
      dataType: 'html',
      success: update_evol,
      complete(data) {
        $('.spinner-border').removeClass('visible').addClass('invisible');
      },
    });
  } else {
    getGeneral();
    $('#csv_button').prop('disabled', true);
    $('#json_button').prop('disabled', true);
  }
});

$('#xModal').on('click', () => {
  $('#errorModal').hide();
});

$('#closeModal').on('click', (e) => {
  $('#errorModal').hide();
});

$('button#line_chart_button').on('click', (e) => {
  let start_date = $('#start_placeholder').attr('placeholder');
  let end_date = $('#end_placeholder').attr('placeholder');
  if ($('#start_placeholder').datepicker('getDate') != null) {
    start_date = $('#start_placeholder').datepicker('getDate');
  }
  if ($('#end_placeholder').datepicker('getDate') != null) {
    end_date = $('#end_placeholder').datepicker('getDate');
  }
  if ((Date.parse(start_date) >= Date.parse(end_date))
       || (Date.parse(start_date) > Date.now())
       || (Date.parse(end_date) > Date.now())) {
    $('#errorModal').show();
  } else {
    start_date = $.format.date(new Date(start_date), 'yyyy-MM-dd');
    end_date = $.format.date(new Date(end_date), 'yyyy-MM-dd');
    if ($('#country-selector').val() != 'Worldwide') {
      const countryCode = $('#country-selector').val();
      const line_dates = { start_date, end_date };
      $.ajax({
        url: `${apiPath}/country/${countryCode}?from=${start_date}&to=${end_date}`,
        type: 'get',
        dataType: 'html',
        success(data) {
          update_line(data, 0);
        },
      });
    } else {
      $.ajax({
        url: `${apiPath}/metrics/active?from=${start_date}&to=${end_date}`,
        type: 'GET',
        success: update_line,
      });
    }
  }
});

$('button#pie_chart_button').on('click', () => {
  const piePlaceholder = $('#pie_placeholder');
  const date = piePlaceholder.datepicker('getDate') || piePlaceholder.attr('placeholder');

  if (Date.parse(date) >= Date.now()) {
    $('#errorModal').show();

    return;
  }

  updatePieChart();
});

// DOWNLOAD BUTTONS
$('#csv_button').on('click', async () => {
  const countryCode = $('#country-selector').val();

  try {
    const response = await fetch(`/download_csv?code=${countryCode}`, {
      responseType: 'blob',
      headers: {
        'Content-Type': 'text/csv',
      },
    });
    const blob = await response.blob();
    download(blob, `${countryCode}_data.csv`);
  } catch (err) {
    console.log(err);
  }
});

$('#json_button').on('click', async () => {
  const countryCode = $('#country-selector').val();
  try {
    const response = await fetch(`/download_json?code=${countryCode}`, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const blob = await response.blob();

    download(blob, `${countryCode}_data.json`);
  } catch (err) {
    console.log(err);
  }
});

// POPULATE GRAPHS WITH GENERAL DATA
function getGeneral() {
  updatePieChart();

  $.ajax({
    url: `${apiPath}/metrics/active`,
    type: 'GET',
    success: update_line,
  });

  $.ajax({
    url: `${apiPath}/metrics/averages`,
    type: 'GET',
    success: update_bar,
  });

  $.ajax({
    url: `${apiPath}/metrics/evols`,
    type: 'GET',
    success: update_evol,
    complete(data) {
      $('.spinner-border').removeClass('visible').addClass('invisible');
    },
  });
}