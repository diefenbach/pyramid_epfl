epfl.Dropdown = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.Dropdown.inherits_from(epfl.ComponentBase);


Object.defineProperty(epfl.ComponentBase.prototype, 'toggle', {
    get: function () {
        return this.elm.children('.toggle');
    }
});


Object.defineProperty(epfl.ComponentBase.prototype, 'menu', {
    get: function () {
        return this.elm.children('ul').find('li > .epfl_dropdown_menuitem');
    }
});


epfl.Dropdown.prototype.after_response = function () {
    var obj = this;

    this.toggle.click(function (event) {
        event.stopImmediatePropagation();
        event.preventDefault();
        $(this).dropdown('toggle');
    });
    this.menu.click(function (event) {
        event.stopImmediatePropagation();
        event.preventDefault();
        var menu_key = $(this).data("menu-key");
        $(this).parent().parent().prev().dropdown('toggle');
        obj.send_event("item_selected", {key: menu_key});
    });
};
