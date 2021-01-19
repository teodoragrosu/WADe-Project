$.getScript("static/js/statistics_page/pie_chart.js");
$.getScript("static/js/statistics_page/line_chart.js");
$.getScript("static/js/statistics_page/active_chart.js");
$.getScript("static/js/statistics_page/bar_chart.js");
$.getScript("static/js/statistics_page/country_data.js");

var noPie = true;
var noLine = true;
var noBar = true

var myPieChart;
var myLineChart;
var myBarChart;

$( function() {
    $( ".date-box" ).datepicker({ format: 'yyyy-mm-dd', startDate: "2020-01-01", endDate: "0" });
});

$("#country-selector").change(function(){
    $('.spinner-border').removeClass('invisible').addClass('visible');
    var countryCode = $("#country-selector").val();

    $.ajax({
        url: "http://127.0.0.1:5000/api/country/"+countryCode,
        type: 'get',
        success: save_country_data
    });
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

        var line_dates = {'start_date': start_date, 'end_date': end_date}
        $.ajax({
            type : 'POST',
            async: false,
            url : "http://127.0.0.1:8000/statistics",
            data : line_dates
        });

        if(noLine){
            $('#waiting1').remove();
            $.ajax({
                url: "http://127.0.0.1:8000/line_data",
                type: 'get',
                dataType: 'html',
                async: false,
                success: generate_line_chart
             });
            noLine=false;
        }
        else {
            $.ajax({
                url: "http://127.0.0.1:8000/line_data",
                type: 'get',
                dataType: 'html',
                async: false,
                success: update_line
            });
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
        $.ajax({
            type : 'POST',
            async: false,
            url : "http://127.0.0.1:8000/statistics",
            data : post_pie_date
        });

        if(noPie){
            $('#waiting2').remove();
            $.ajax({
                url: "http://127.0.0.1:8000/pie_data",
                type: 'get',
                dataType: 'html',
                async: false,
                success: generate_pie_chart
             });
            noPie=false;

            // To EDIT THIS with request data
            $.ajax({
                url: "http://127.0.0.1:8000/pie_data",
                type: 'get',
                dataType: 'html',
                async: false,
                success: generate_active_chart
             });

             $.ajax({
                url: "http://127.0.0.1:8000/bar_data",
                type: 'get',
                dataType: 'html',
                async: false,
                success: generate_bar_chart
             });
        }
        else {
            $.ajax({
                url: "http://127.0.0.1:8000/pie_data",
                type: 'get',
                dataType: 'html',
                async: false,
                success: update_pie
            });
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