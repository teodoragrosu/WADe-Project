function save_country_data(country_data) {
    var cdata = {'country_data': country_data}
    $.ajax({
        url: "http://127.0.0.1:8000/country_data",
        type: 'POST',
        async: false,
        data: cdata,
        success: function(data) {
            $('.spinner-border').removeClass('visible').addClass('invisible');
        }
    });
}