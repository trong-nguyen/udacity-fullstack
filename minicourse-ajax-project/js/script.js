
function loadData(event) {
    event.preventDefault();

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    // YOUR CODE GOES HERE!

    // load streetview

    var street = $('#street').val();
    var city = $('#city').val();

    $greeting.text('So you want to live at ' + street + ', ' + city + '?');

    var url = 'http://maps.googleapis.com/maps/api/streetview?size=600x300&location=';
    url += street + ', ' + city;
    url = encodeURI(url);

    $('#bgimg').attr('src', url);

    // NYT requests

    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json";
    url = url + '?' + $.param({
        'api-key': '6d988bc46c184ba18d71ed6ca437a624',
        'q': city
    });

    $.getJSON(url, function (articles) {
        var ha = articles.response.docs.map(function (a) {
            return {
                url: a['web_url'],
                title: a.headline.main
            };
        });

        var list = ha.map(function (article) {
            var $li = $('<li></li>');
            $li.append(
                $('<a></a>')
                    .attr('href', article.url)
                    .text(article.title)
                );
            return $li;
        });

        $nytElem.empty().append(list);
    });

    return false;
};

$('#form-container').submit(loadData);
