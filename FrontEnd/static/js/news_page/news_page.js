var page = 1;
var searchTerm = '';
var publicationTerm = '';
var numberOfResults = 0;

var urlParams = new URLSearchParams(window.location.search);
if(urlParams.has('keyword')){
    searchTerm = urlParams.get('keyword');
    $("#searchTermInput").val(searchTerm);
}

function refreshData(){
    $.ajax({url: "http://127.0.0.1:5000/api/news/page/" + page +"?search_term=" + searchTerm + "&publication=" + publicationTerm, success: function(result){
        var news = JSON.parse(result);
        numberOfResults = Object.keys(news).length;
        var divHtml = '';
        for(var i in news){
            var item = news[i];
            var keywordsHtml = '';
            var publishedByHtml = '';
            var imgHtml = '';

            if(item.img_url.length > 0 && item.img_url != "None"){
                imgHtml = `<img class="card-img-top" src="${item.img_url}" alt="image">`;
            }

            if(item.publication != "None"){
                publishedByHtml = `<div class="col-5"><small>Published by: ${ item.publication }</small></div>`;
            }

            if(item.keywords.length > 0 && item.keywords[0] != "" ){
                var keywordsInnerHtml = "";
                for( var keyword in item.keywords){
                    keywordsInnerHtml += `<a href="http://127.0.0.1:8000/news?keyword=${item.keywords[keyword]}">${ item.keywords[keyword] } </a>`
                }
                keywordsHtml = `<div class="card-footer text-muted"> Some keywords: ${keywordsInnerHtml}</div>`
            }

            var itemHtml = `
                <div class="card mb-4">
                ${imgHtml}
                    <div class="card-body">
                      <div class="row">
                          <div class="col-7"><small>Published at: ${ formatDate(item.date) }</small></div>
                          ${publishedByHtml}
                      </div>
                      <h2 class="card-title">${ item.title }</h2>
                      <div>
                      ${keywordsHtml}
                      </div>
                      <a href="${item["source"]}" target="_blank" class="btn btn-primary">Read More &rarr;</a>
                    </div>
                </div>`;
            divHtml += itemHtml;
         }

        $("#newsList").html(divHtml);
        updatePaginationButtons();
    }});
}

function updatePaginationButtons(){
    if(page > 1){
        $("#previousPageLi").removeClass("disabled");
    } else {
        $("#previousPageLi").addClass("disabled");
    }

    if(numberOfResults == 10){
        $("#nextPageLi").removeClass("disabled");
    } else {
        $("#nextPageLi").addClass("disabled");
    }
}

function formatDate(date) {
    var d = new Date(date);
    var month = (d.getMonth() + 1).toString();
    var day = d.getDate().toString();
    var year = d.getFullYear().toString();
    var hours = d.getHours().toString();
    var minutes = d.getMinutes().toString();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;
    if (hours.length < 2)
        hours = '0' + hours;
    if (minutes.length < 2)
        minutes = '0' + minutes;

    return `${hours}:${minutes} ${day}.${month}.${year}`;
}


$("#previousPage").click(function(){
    page--;
    refreshData();
});

$("#nextPage").click(function(){
    page++;
    refreshData();
});

$("#searchTermButton").click(function(){
    page = 1;
    searchTerm = $("#searchTermInput").val();
    refreshData();
});

$("#publicationButton").click(function(){
    page = 1;
    publicationTerm = $("#publicationInput").val();
    refreshData();
});


refreshData();