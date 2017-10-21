
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
            var $li = $('<li>');
            $li.append(
                $('<a>')
                    .attr('href', article.url)
                    .text(article.title)
                );
            return $li;
        });

        $nytElem.empty().append(list);
    })
    .fail(function (event) {
        $nytElem.empty().text('Could not load NYT articles');
    });

    // Wikipedia request
    function getFeeds(searchText) {
        var endpoint = "https://en.wikipedia.org/w/api.php?";
        var params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|info|pageimages",
            "generator": "search",
            "exintro": 1,
            // "explaintext": 1,
            "exsectionformat": "wiki",
            "inprop": "url",
            "piprop": "thumbnail",
            "pithumbsize": "300",
            "pilicense": "any",
            "gsrlimit": "20",
            "gsrsearch": ""
        };

        params.gsrsearch = encodeURIComponent(searchText);
        // var cors = "https://crossorigin.me/";
        var cors = ""; //"http://cors-anywhere.herokuapp.com/";
        var url = cors + endpoint + $.param(params) + '&callback=?';
        X = $.getJSON(url);
        return X;
    }

    getFeeds(city)
        .done(function (result) {
            var articles = result.query.pages;

            var ha = $.map(articles, function (a) {
                return {
                    url: a.fullurl,
                    title: a.title,
                    sneak: a.extract
                };
            });

            var list = ha.map(function (article) {
                var $li = $('<li>');
                $li.append(
                    $('<a>')
                        .attr('href', article.url)
                        .text(article.title)
                    )
                    // .append(article.sneak)
                    ;
                return $li;
            });

            $wikiElem.empty().append(list);
        })
        .fail(function (reason) {
            $wikiElem.empty().append('Error getting Wikipedia, error');
            console.log('Error getting Wikipedia, error', reason);
        });

    return false;
};

$('#form-container').submit(loadData);
