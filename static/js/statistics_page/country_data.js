function save_country_data(country_data) {
    var cdata = {'country_data': country_data}
    $.ajax({
        url: "https://coda-fe.herokuapp.com/country_data",
        type: 'POST',
        async: false,
        data: cdata,
        success: function(data) {
            $('.spinner-border').removeClass('visible').addClass('invisible');
            $('#csv_button').prop("disabled", false);
            $('#json_button').prop("disabled", false);
        }
    });
}