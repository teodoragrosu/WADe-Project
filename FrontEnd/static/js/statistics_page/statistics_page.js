$.getScript("static/js/statistics_page/pie_chart.js");
$.getScript("static/js/statistics_page/line_chart.js");
$.getScript("static/js/statistics_page/active_chart.js");

$.getScript("static/js/statistics_page/country_data.js");

var noPie = true;
var noLine = true;

var myPieChart;
var myLineChart;

console.log('LOADED');
$("#country-selector").change(function(){
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
    var start_date1 = $('#start_placeholder').attr('placeholder');
    var end_date1 = $('#end_placeholder').attr('placeholder');

    if($('#start_date1').datepicker('getDate') != null){
        start_date1 = $('#start_date1').datepicker('getDate');
    }
    if($('#end_date1').datepicker('getDate') != null){
        end_date1 = $('#end_date1').datepicker('getDate');
    }

    if((Date.parse(start_date1) >= Date.parse(end_date1)) ||
       (Date.parse(start_date1) > Date.now()) ||
       (Date.parse(end_date1) > Date.now())){
        $('#errorModal').show();
    }
    else {
        start_date1 = new Date(start_date1).toLocaleDateString();
        end_date1 = new Date(end_date1).toLocaleDateString();

        var line_dates = {'start_date1': start_date1, 'end_date1': end_date1}
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
    var stats_date = $('#stats_placeholder').attr('placeholder');

    if($('#stats_date').datepicker('getDate') != null){
        stats_date = $('#stats_date').datepicker('getDate');
    }

    if(Date.parse(stats_date) >= Date.now()) {
        $('#errorModal').show();
    }
    else {
        stats_date = new Date(stats_date).toLocaleDateString();
        var pie_date = {'stats_date': stats_date}
        $.ajax({
            type : 'POST',
            async: false,
            url : "http://127.0.0.1:8000/statistics",
            data : pie_date
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
            $.ajax({
                url: "http://127.0.0.1:8000/pie_data",
                type: 'get',
                dataType: 'html',
                async: false,
                success: generate_active_chart
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