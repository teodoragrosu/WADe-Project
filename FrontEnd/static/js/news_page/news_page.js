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
    $.ajax({url: "https://coda-apiv1.herokuapp.com/api/news/page/" + page +"?search_term=" + searchTerm + "&publication=" + publicationTerm, success: function(result){
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
                    keywordsInnerHtml += `<a href="https://coda-fe.herokuapp.com/news?keyword=${item.keywords[keyword]}">${ item.keywords[keyword] } </a>`
                }
                keywordsHtml = `<div class="card-footer text-muted"> Keywords: ${keywordsInnerHtml}</div>`
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
                          <div class="read-share">
                                <a href="${item["source"]}" target="_blank" class="btn btn-primary">Read More &rarr;</a>
                                <div id="share-buttons">
                                    <a href="mailto:?Subject=Check this article I found on CODA&amp;Body=I%20saw%20this%20and%20thought%20you%20might%20enjoy%20it: ${item["source"]}">
                                        <img src="https://simplesharebuttons.com/images/somacro/email.png" alt="Email" />
                                    </a>
                                    <a href="http://www.facebook.com/sharer.php?u=${item["source"]}" target="_blank">
                                        <img src="https://simplesharebuttons.com/images/somacro/facebook.png" alt="Facebook" />
                                    </a>
                                    <a href="http://www.linkedin.com/shareArticle?mini=true&amp;url=${item["source"]}" target="_blank">
                                        <img src="https://simplesharebuttons.com/images/somacro/linkedin.png" alt="LinkedIn" />
                                    </a>
                                    <a href="http://reddit.com/submit?url=${item["source"]}&amp;title=${ item.title }" target="_blank">
                                        <img src="https://simplesharebuttons.com/images/somacro/reddit.png" alt="Reddit" />
                                    </a>
                                    <a href="https://twitter.com/share?url=${item["source"]}&amp;text=Coda%20article%20&amp;hashtags=coda" target="_blank">
                                        <img src="https://simplesharebuttons.com/images/somacro/twitter.png" alt="Twitter" />
                                    </a>
                                </div>
                          </div>
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

    $("#pageNumber").html(page);
    window.scrollTo(0, 0);
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