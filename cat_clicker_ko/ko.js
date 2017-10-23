var allCatData = [
    {
        picture: "https://media1.giphy.com/media/yXPquATCb8kGk/200_s.gif",
        name: "Luffy",
        nickNames: ["Luff"],
        clicks: 1
    },
    {
        picture: "https://i.ytimg.com/vi/W-PBFMECvTE/maxresdefault.jpg",
        name: "Zebra",
        nickNames: ["Bic"],
        clicks: 1
    },
    {
        picture: "https://i.pinimg.com/736x/2e/18/ab/2e18ab3f71b73c6719b04c81625bb922--cat-cute-cute-pets.jpg",
        name: "Mumbo",
        nickNames: ["Mum"],
        clicks: 1
    },
    {
        picture: "https://i.pinimg.com/736x/ba/03/23/ba03237a6d6499f0e2633314826e1526--cutest-animals-baby-animals.jpg",
        name: "Jerry",
        nickNames: ["Jeff"],
        clicks: 1
    },
];

var CatModel = function (species) {
    this.name = ko.observable(species['name']);
    this.url = ko.observable(species['picture']);
    this.clicks = ko.observable(species['clicks']);
    this.level = ko.computed(function () {
        if (this.clicks() < 10) {
            return 'Infant';
        } else if (this.clicks() < 20) {
            return 'Teen';
        }
        return 'Adult';
    }, this);

    this.nickNames = ko.observableArray(species['nickNames']);
};

var ViewModel = function () {
    var self = this;

    this.catList = ko.observableArray([]);
    allCatData.forEach(function (data) {
        self.catList.push(new CatModel(data));
    });

    this.catModel = ko.observable(this.catList()[0]);

    this.increaseClicks = function () {
        self.catModel().clicks(self.catModel().clicks() + 1);
    };

};

var vm = new ViewModel();
ko.applyBindings(vm);

setTimeout(function () {
    vm.catModel().name('Tommy the great');
    vm.catModel().nickNames.push('Alexander the Great');
}, 2000);


