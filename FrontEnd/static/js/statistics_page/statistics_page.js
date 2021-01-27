var apiPath = 'https://coda-apiv1.herokuapp.com/api'
//var apiPath = 'http://127.0.0.1:5000/api'

$.getScript("static/js/statistics_page/line_chart.js",
function() {$.ajax({
            url: apiPath + "/metrics/active",
            type: 'GET',
            success:generate_line_chart});
            });
$.getScript("static/js/statistics_page/pie_chart.js",
function() {$.ajax({
            url: apiPath + "/metrics/pie",
            type: 'GET',
            success:generate_pie_chart});
            });
$.getScript("static/js/statistics_page/bar_chart.js",
function() {$.ajax({
            url: apiPath + "/metrics/averages",
            type: 'GET',
            success:generate_bar_chart});
            });
$.getScript("static/js/statistics_page/evol_chart.js",
function() {$.ajax({
            url: apiPath + "/metrics/evols",
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
            url: apiPath + "/metrics/totals",
            type: 'GET',
            success:generate_totals_chart});
            });

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
            $('#csv_button').prop("disabled", false);
            $('#json_button').prop("disabled", false);
            $.ajax({
                url: apiPath + "/country/" + countryCode,
                type: 'get',
                dataType: 'html',
                success: function(data){
                    update_line(data);
                    update_pie(data);
                    update_evol(data);
                }
             });
            $.ajax({
                url: apiPath + "/country/monthly/" + countryCode,
                type: 'get',
                dataType: 'html',
                success: update_bar
            });
    }
    else {
        getGeneral();
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
            var countryCode = $("#country-selector").val();
            var line_dates = {'start_date': start_date, 'end_date': end_date}
            $.ajax({
                url: apiPath + "/country/" + countryCode + "?from=" + start_date + "&to=" + end_date,
                type: 'get',
                dataType: 'html',
                success: function (data){
                    update_line(data, 0);
                }
            });
        }
        else {
            $.ajax({
            url: apiPath + "/metrics/active?from="+start_date+"&to="+end_date,
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
                url: apiPath + "/country/" + countryCode,
                type: 'get',
                dataType: 'html',
                success: update_pie
            });
        }
        else {
            $.ajax({
            url: apiPath + "/metrics/pie?date="+pie_date,
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

//DOWNLOAD BUTTONS

$('#csv_button').on('click', function (e) {
    var countryCode = $("#country-selector").val();
    const options={
        method: "GET",
        headers:{
            'Content-Type':'text/csv',
        },
        responseType: 'blob'
    };

    fetch('/download_csv?code='+countryCode,options)
        .then(res=>{
            return res.blob();
        }).then(blob=>{
            download(blob,countryCode+"_data.csv")
        }).catch(err=>console.log(err));
});

$('#json_button').on('click', function (e) {
    var countryCode = $("#country-selector").val();
    const options={
        method: "GET",
        headers:{
            'Content-Type':'application/json',
        }
    };

    fetch('/download_json?code='+countryCode,options)
        .then(res=>{
            return res.blob();
        }).then(blob=>{
            download(blob, countryCode+"_data.json")
        }).catch(err=>console.log(err));
});

//POPULATE GRAPHS WITH GENERAL DATA
function getGeneral() {
    $.ajax({
            url: apiPath + "/metrics/active",
            type: 'GET',
            success:update_line
            });
    $.ajax({
            url: apiPath + "/metrics/pie",
            type: 'GET',
            success:update_pie
            });
    $.ajax({
            url: apiPath + "/metrics/averages",
            type: 'GET',
            success:update_bar
            });
    $.ajax({
            url: apiPath + "/metrics/evols",
            type: 'GET',
            success: update_evol,
            complete: function(data) {
                $('.spinner-border').removeClass('visible').addClass('invisible');
            }
            });
}