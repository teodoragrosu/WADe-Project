var page = 1;
var searchTerm = '';
var numberOfResults = 0;

function refreshData(){
    var categoryQueryParam = "categories=" + selectedCategories.join("&categories=")
    $.ajax({url: "http://127.0.0.1:5000/api/news/page/" + page +"?search_term=" + searchTerm + "&" + categoryQueryParam, success: function(result){
        console.log(selectedCategories);
        var articles = JSON.parse(result);
        numberOfResults = Object.keys(articles).length;
        var divHtml = '';
        for(var key in articles){
            var article = articles[key];
            var authorsHtml = '';
            var categoriesHtml = '';

            if(article.authors.length > 0 && article.authors[0] != "None" ){
                authorsHtml = article.authors.join(", ");
                if(authorsHtml.length > 50){
                    authorsHtml = authorsHtml.substring(0,50) + "...";
                }
                authorsHtml = `<small>By ${authorsHtml}</small>`
            }

            if(article.categories.length > 0 && article.categories[0] != "" ){
                var categoriesInnerHtml = "";
                for( var category in article.categories){
                    categoriesInnerHtml += `<a href="http://127.0.0.1:8000/articles?category=${article.categories[category]}">${ article.categories[category] } </a>`
                }
                categoriesHtml = `<div class="card-footer text-muted"> Categories: ${categoriesInnerHtml}</div>`
            }

            var itemHtml = `
                <div class="card mb-4">
                    <div class="card-body">
                      <small>Published at: ${ formatDate(article.date) }</small>
                      <h2 class="card-title">${ article.title }
                      ${authorsHtml}
                      </h2>
                      <p class="card-text">${ article.abstract }</p>
                      <a href="${article["url"]}" target="_blank" class="btn btn-primary">Read More &rarr;</a>
                    </div>
                    ${categoriesHtml}
                </div>`;
            divHtml += itemHtml;
               }

        $("#articlesList").html(divHtml);
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


refreshData();