var main = (function () {
    var model = (function() {
        var cats = [
            {
                picture: "https://media1.giphy.com/media/yXPquATCb8kGk/200_s.gif",
                name: "Luffy"
            },
            {
                picture: "https://i.ytimg.com/vi/W-PBFMECvTE/maxresdefault.jpg",
                name: "Zebra"
            },
            {
                picture: "https://i.pinimg.com/736x/2e/18/ab/2e18ab3f71b73c6719b04c81625bb922--cat-cute-cute-pets.jpg",
                name: "Mumbo"
            },
            {
                picture: "https://i.pinimg.com/736x/ba/03/23/ba03237a6d6499f0e2633314826e1526--cutest-animals-baby-animals.jpg",
                name: "Jerry"
            },
        ];

        var currentCat = 0;

        return {
            cats: cats,

            init: function () {
                cats.forEach(function (cat) {
                    cat.clicks = 0;
                });
            },

            getCurrentCat: function () {
                return cats[currentCat];
            },

            setCurrentCat: function (id) {
                if (id >= 0 && id < cats.length) {
                    currentCat = id;
                } else {
                    console.log('invalid cat id', id);
                }
            },

            increaseCurrentCatClicks: function () {
                ++cats[currentCat].clicks;
            }
        }
    })();

    // utility functions
    function removeChildren (elm) {
        elm.innerHTML = "";
    }

    function getFirstByClass (elm, cls) {
        return elm.getElementsByClassName(cls)[0];
    }


    var catCollectionView = (function () {
        var $collection = document.getElementById('cat-collection');
        var singleCatTemplate = $collection.firstElementChild.cloneNode(true);

        return {
            elm: $collection,
            render: function (collection) {
                var cats = collection.map(function (catData, idx) {
                    var cat = singleCatTemplate.cloneNode(true);
                    var catButton = cat.getElementsByTagName('button')[0];
                    catButton.textContent = catData.name;
                    catButton.id = idx;
                    return cat;
                });

                removeChildren($collection);
                cats.forEach(function (cat) {
                    $collection.append(cat);
                });
            }
        };
    })();

    var catView = (function () {
        // Grasping Dom Elements and initial templates
        var $elm = document.getElementById('cat-view');

        return {
            elm: $elm,
            render: function(cat) {
                getFirstByClass($elm, 'cat-name').textContent = cat.name;
                getFirstByClass($elm, 'cat-picture').setAttribute('src', cat.picture);
                getFirstByClass($elm, 'cat-clicks').textContent = cat.clicks;
            }
        };

    })();

    var octopus = (function () {
        function setCurrentCat (id) {
            var id = Number(id);
            if (id < model.cats.length) {
                model.setCurrentCat(id);
                catView.render(model.getCurrentCat());
            } else {
                console.log('Error setting cat current', id);
            }
        };

        return {
            init: function () {
                model.init();

                catCollectionView.render(model.cats);
                setCurrentCat(0);

                var pic = catView.elm.getElementsByClassName('cat-picture')[0];
                pic.addEventListener('click', function (event) {
                    model.increaseCurrentCatClicks();
                    catView.render(model.getCurrentCat());
                });

                catCollectionView.elm.addEventListener('click', function (event) {
                    console.log(event.target.id);
                    setCurrentCat(event.target.id);
                });
            }
        };
    })();

    return octopus;
})();

main.init();