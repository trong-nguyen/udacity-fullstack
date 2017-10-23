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
            init: function () {
                cats.forEach(function (cat) {
                    cat.clicks = 0;
                });
            },

            getAllCats: function () {
                return cats;
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
            },

            updateCat: function (details) {
                // return true if successfully updated
                // false if not

                var cat = cats[currentCat];

                details.clicks = Number(details.clicks);

                if (details.name !== undefined &&
                    details.picture !== undefined &&
                    details.clicks !== undefined &&
                    details.clicks === details.clicks) {

                    ['name', 'picture', 'clicks'].forEach(function (x) {
                        cat[x] = details[x];
                    });

                    return true;
                } else {
                    return false;
                }
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

    var adminView = (function () {
        var $elm = document.getElementById('admin-view');
        var $adminForm = document.getElementById('admin-form');

        return {
            adminForm: $adminForm,
            adminBtn: document.getElementById('btn-admin'),
            submitBtn: document.getElementById('btn-submit'),
            cancelBtn: document.getElementById('btn-cancel'),

            render: function (cat) {
                document.getElementById('i-cat-name').value = cat.name;
                document.getElementById('i-cat-picture').value = cat.picture;
                document.getElementById('i-cat-clicks').value = cat.clicks;
            },

            getCatInputs: function () {
                return {
                    name: document.getElementById('i-cat-name').value,
                    picture: document.getElementById('i-cat-picture').value,
                    clicks: document.getElementById('i-cat-clicks').value,
                }
            }
        };
    })();

    var octopus = (function () {
        function setCurrentCat (id) {
            var id = Number(id);
            if (id < model.getAllCats().length) {
                model.setCurrentCat(id);
                catView.render(model.getCurrentCat());
                adminView.render(model.getCurrentCat());
            } else {
                console.log('Error setting cat current', id);
            }
        };

        function showAdmin () {
            adminView.render(model.getCurrentCat());
            adminView.adminForm.hidden = false;
            adminView.adminBtn.hidden = true;
        };

        function hideAdmin() {
            adminView.adminForm.hidden = true;
            adminView.adminBtn.hidden = false;
        }

        return {
            init: function () {
                model.init();

                catCollectionView.render(model.getAllCats());
                setCurrentCat(0);

                var pic = catView.elm.getElementsByClassName('cat-picture')[0];
                pic.addEventListener('click', function (event) {
                    model.increaseCurrentCatClicks();
                    var cc = model.getCurrentCat();
                    catView.render(cc);
                    adminView.render(cc);
                });

                catCollectionView.elm.addEventListener('click', function (event) {
                    setCurrentCat(event.target.id);
                });

                // open admin forms
                adminView.adminBtn.addEventListener('click', function (event) {
                    event.preventDefault();
                    showAdmin();
                    return false;
                });

                // submit updates
                adminView.submitBtn.addEventListener('click', function (event) {
                    event.preventDefault();

                    var details = adminView.getCatInputs();
                    if (model.updateCat(details)) {
                        var cat = model.getCurrentCat();
                        adminView.render(cat);
                        catView.render(cat);
                        catCollectionView.render(model.getAllCats());
                    } else {
                        console.log('Failed to update cat with details', details);
                    }

                    return false;
                });

                // close admin forms
                adminView.cancelBtn.addEventListener('click', function (event) {
                    event.preventDefault();
                    hideAdmin();
                    return false;
                });
            }
        };
    })();

    return octopus;
})();

main.init();