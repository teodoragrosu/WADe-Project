$.getScript("static/js/statistics_page/line_chart.js",
function() {$.ajax({
            url: "https://coda-apiv1.herokuapp.com/api/metrics/active",
            type: 'GET',
            success:generate_line_chart});
            });
$.getScript("static/js/statistics_page/pie_chart.js",
function() {$.ajax({
            url: "https://coda-apiv1.herokuapp.com/api/metrics/pie",
            type: 'GET',
            success:generate_pie_chart});
            });
$.getScript("static/js/statistics_page/bar_chart.js",
function() {$.ajax({
            url: "https://coda-apiv1.herokuapp.com/api/metrics/averages",
            type: 'GET',
            success:generate_bar_chart});
            });
$.getScript("static/js/statistics_page/evol_chart.js",
function() {$.ajax({
            url: "https://coda-apiv1.herokuapp.com/api/metrics/evols",
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
            url: "https://coda-apiv1.herokuapp.com/api/metrics/totals",
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
//        $.ajax({
//            url: "https://coda-apiv1.herokuapp.com/api/country/"+countryCode+"/download?format=json",
//            type: 'GET'
//        });
//        $.ajax({
//            url: "https://coda-apiv1.herokuapp.com/api/country/"+countryCode+"/download?format=csv",
//            type: 'GET'
//        })
        $.ajax({
            url: "https://coda-apiv1.herokuapp.com/api/country/"+countryCode,
            type: 'GET',
            success: save_country_data,
            complete: function(){
                $.ajax({
                    url: "https://coda-fe.herokuapp.com/line_data",
                    type: 'get',
                    dataType: 'html',
                    success: update_line
                 });
                $.ajax({
                    url: "https://coda-fe.herokuapp.com/pie_data",
                    type: 'get',
                    dataType: 'html',
                    success: update_pie
                 });
                $.ajax({
                    url: "https://coda-apiv1.herokuapp.com/api/country/monthly/"+countryCode,
                    type: 'get',
                    dataType: 'html',
                    async: false,
                    success: update_bar
                });
                $.ajax({
                    url: "https://coda-fe.herokuapp.com/evol_data",
                    type: 'get',
                    dataType: 'html',
                    async: false,
                    success: update_evol
                });
            }
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
            var line_dates = {'start_date': start_date, 'end_date': end_date}
            $.ajax({
                type : 'POST',
                async: false,
                url : "https://coda-fe.herokuapp.com/statistics",
                data : line_dates
            });

            $.ajax({
                url: "https://coda-fe.herokuapp.com/line_data",
                type: 'get',
                dataType: 'html',
                async: false,
                success: update_line
            });
        }
        else {
            $.ajax({
            url: "https://coda-apiv1.herokuapp.com/api/metrics/active?from="+start_date+"&to="+end_date,
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
                url : "https://coda-fe.herokuapp.com/statistics",
                data : post_pie_date
            });

            $.ajax({
                url: "https://coda-fe.herokuapp.com/pie_data",
                type: 'get',
                dataType: 'html',
                async: false,
                success: update_pie
            });
        }
        else {
            $.ajax({
            url: "https://coda-apiv1.herokuapp.com/api/metrics/pie?date="+pie_date,
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
            url: "https://coda-apiv1.herokuapp.com/api/metrics/active",
            type: 'GET',
            success:update_line
            });
    $.ajax({
            url: "https://coda-apiv1.herokuapp.com/api/metrics/pie",
            type: 'GET',
            success:update_pie
            });
    $.ajax({
            url: "https://coda-apiv1.herokuapp.com/api/metrics/averages",
            type: 'GET',
            success:update_bar
            });
    $.ajax({
            url: "https://coda-apiv1.herokuapp.com/api/metrics/evols",
            type: 'GET',
            success: update_evol,
            complete: function(data) {
                $('.spinner-border').removeClass('visible').addClass('invisible');
            }
            });
}