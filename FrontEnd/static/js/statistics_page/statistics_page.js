$.getScript("static/js/statistics_page/line_chart.js",
function() {$.ajax({
            url: "http://127.0.0.1:5000/api/metrics/active",
            type: 'GET',
            success:generate_line_chart});
            });
$.getScript("static/js/statistics_page/pie_chart.js",
function() {$.ajax({
            url: "http://127.0.0.1:5000/api/metrics/pie",
            type: 'GET',
            success:generate_pie_chart});
            });
$.getScript("static/js/statistics_page/bar_chart.js",
function() {$.ajax({
            url: "http://127.0.0.1:5000/api/metrics/averages",
            type: 'GET',
            success:generate_bar_chart});
            });
$.getScript("static/js/statistics_page/evol_chart.js",
function() {$.ajax({
            url: "http://127.0.0.1:5000/api/metrics/evols",
            type: 'GET',
            success:generate_evol_chart,
            complete: function (data) {
                    $('#mainLoader').addClass('invisible');
                    $('#layoutSidenav_content').removeClass('invisible').addClass('visible');
            }
            });
            });
$.getScript("static/js/statistics_page/totals_chart.js",
function() {$.ajax({
            url: "http://127.0.0.1:5000/api/metrics/totals",
            type: 'GET',
            success:generate_totals_chart});
            });
$.getScript("static/js/statistics_page/country_data.js");

var myTotalsChart;
var myPieChart;
var myLineChart;
var myBarChart;
var myEvolChart;

$( function() {
    $( ".date-box" ).datepicker({ format: 'yyyy-mm-dd', startDate: "2020-01-01", endDate: "0" });
});

$("#country-selector").change(function(){
    $('.spinner-border').removeClass('invisible').addClass('visible');
    var countryCode = $("#country-selector").val();
    if (countryCode != 'ALL'){
        $.ajax({
            url: "http://127.0.0.1:5000/api/country/"+countryCode,
            type: 'GET',
            success: save_country_data,
            complete: function(){
                $.ajax({
                    url: "http://127.0.0.1:8000/line_data",
                    type: 'get',
                    dataType: 'html',
                    success: update_line
                 });
                $.ajax({
                    url: "http://127.0.0.1:8000/pie_data",
                    type: 'get',
                    dataType: 'html',
                    success: update_pie
                 });
                $.ajax({
                    url: "http://127.0.0.1:8000/bar_data",
                    type: 'get',
                    dataType: 'html',
                    async: false,
                    success: update_bar
                });
                $.ajax({
                    url: "http://127.0.0.1:8000/evol_data",
                    type: 'get',
                    dataType: 'html',
                    async: false,
                    success: update_evol
                });
            }
        });
    }
    else {
        $('#csv_button').prop("disabled", true);
        $('#json_button').prop("disabled", true);
    }
});

$('#xModal').on('click', function (e) {
    $('#errorModal').hide();
});

$('#closeModal').on('click', function (e) {
    $('#errorModal').hide();
});

$('button#line_chart_button').on('click', function (e) {
    var start_date = $('#start_placeholder').attr('placeholder');
    var end_date = $('#end_placeholder').attr('placeholder');

    if($('#start_placeholder').datepicker('getDate') != null){
        start_date = $('#start_placeholder').datepicker('getDate');
    }
    if($('#end_placeholder').datepicker('getDate') != null){
        end_date = $('#end_placeholder').datepicker('getDate');
    }

    if((Date.parse(start_date) >= Date.parse(end_date)) ||
       (Date.parse(start_date) > Date.now()) ||
       (Date.parse(end_date) > Date.now())){
        $('#errorModal').show();
    }
    else {
        start_date = $.format.date(new Date(start_date),'yyyy-MM-dd');
        end_date = $.format.date(new Date(end_date),'yyyy-MM-dd');

        if($("#country-selector").val() != 'ALL') {
            var line_dates = {'start_date': start_date, 'end_date': end_date}
            $.ajax({
                type : 'POST',
                async: false,
                url : "http://127.0.0.1:8000/statistics",
                data : line_dates
            });

            $.ajax({
                url: "http://127.0.0.1:8000/line_data",
                type: 'get',
                dataType: 'html',
                async: false,
                success: update_line
            });
        }
        else {
            $.ajax({
            url: "http://127.0.0.1:5000/api/metrics/active?from="+start_date+"&to="+end_date,
            type: 'GET',
            success: update_line});
        }
    }
});

$('button#pie_chart_button').on('click', function (e) {
    var pie_date = $('#pie_placeholder').attr('placeholder');

    if($('#pie_placeholder').datepicker('getDate') != null){
        pie_date = $('#pie_placeholder').datepicker('getDate');
    }

    if(Date.parse(pie_date) >= Date.now()) {
        $('#errorModal').show();
    }
    else {
        pie_date = $.format.date(new Date(pie_date),'yyyy-MM-dd');
        var post_pie_date = {'pie_date': pie_date}

        if($("#country-selector").val() != 'ALL') {
            $.ajax({
                type : 'POST',
                async: false,
                url : "http://127.0.0.1:8000/statistics",
                data : post_pie_date
            });

            $.ajax({
                url: "http://127.0.0.1:8000/pie_data",
                type: 'get',
                dataType: 'html',
                async: false,
                success: update_pie
            });
        }
        else {
            $.ajax({
            url: "http://127.0.0.1:5000/api/metrics/pie?date="+pie_date,
            type: 'GET',
            success: update_pie});
        }
    }
});

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [year, month, day].join('-');
}

$('#csv_button').on('click', function (e) {
    var countryCode = $("#country-selector").val();
    $.ajax({
            url: "http://127.0.0.1:5000/api/country/"+countryCode+"/download?format=csv",
            type: 'GET',
            complete: function(){
                console.log(data);
            });
});

$('#json_button').on('click', function (e) {
    var countryCode = $("#country-selector").val();
    $.ajax({
            url: "http://127.0.0.1:5000/api/country/"+countryCode+"/download?format=json",
            type: 'GET',
            success: function(data) {
                console.log(data);
            }
    });
});