var octopus = (function main() {
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
            currentCat: currentCat,
            init: function () {
                cats.forEach(function (cat) {
                    cat.clicks = 0;
                });
            }
        }
    })();

    var view = (function () {
        // Grasping Dom Elements and initial templates
        var $collection = document.getElementById('cat-collection');
        var singleCatTemplate = $collection.firstElementChild.cloneNode();
        var $catView = document.getElementById('cat-view');


        function removeChildren (elm) {
            elm.innerHTML = "";
        }

        function getFirstByClass (elm, cls) {
            return elm.getElementsByClassName(cls)[0];
        }

        return {
            collection: $collection,
            catView: $catView,

            renderCatCollection: function (collection) {
                var cats = collection.map(function (catData, idx) {
                    var cat = singleCatTemplate.cloneNode();
                    cat.textContent = catData.name;
                    cat.id = idx;
                    return cat;
                });

                removeChildren($collection);
                cats.forEach(function (cat) {
                    $collection.append(cat);
                });
            },

            renderCatView: function(cat) {
                getFirstByClass($catView, 'cat-name').textContent = cat.name;
                getFirstByClass($catView, 'cat-picture').setAttribute('src', cat.picture);
                getFirstByClass($catView, 'cat-clicks').textContent = cat.clicks;
            }
        }
    })();

    var octopus = new (function () {
        function setCurrentCat (id) {
            var id = Number(id);
            if (id < model.cats.length) {
                model.currentCat = id;
                view.renderCatView(model.cats[id]);
            } else {
                console.log('Error setting cat current', id);
            }
        };

        this.init = function () {
            model.init();

            view.renderCatCollection(model.cats);
            setCurrentCat(0);

            var pic = view.catView.getElementsByClassName('cat-picture')[0];
            pic.addEventListener('click', function (event) {
                ++model.cats[model.currentCat].clicks;
                view.renderCatView(model.cats[model.currentCat]);
            });

            view.collection.addEventListener('click', function (event) {
                console.log(event.target.id);
                setCurrentCat(event.target.id);
            });
        };
    })();

    return octopus;
})();

octopus.init();