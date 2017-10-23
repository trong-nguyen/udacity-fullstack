var viewModel = new (function () {
    this.name = ko.observable('Jerry');
    this.url = ko.observable('https://i.pinimg.com/736x/2e/18/ab/2e18ab3f71b73c6719b04c81625bb922--cat-cute-cute-pets.jpg');
    this.clicks = ko.observable(19);
    this.level = ko.computed(function () {
        if (this.clicks < 10) {
            return 'Infant';
        } else if (this.clicks < 20) {
            return 'Teen';
        }
        return 'Adult';
    }, this);

    this.increaseClicks = function () {
        this.clicks(this.clicks() + 1);
    };

    this.nickNames = ko.observableArray(['the Cat', 'the Jumbo', 'the Monster']);
})();

ko.applyBindings(viewModel);

setTimeout(function () {
    viewModel.name('Tommy the great');
    viewModel.nickNames.push('Alexander the Great');
}, 2000);