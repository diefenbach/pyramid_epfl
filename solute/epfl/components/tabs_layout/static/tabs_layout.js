epfl.TabsLayout = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.TabsLayout.inherits_from(epfl.ComponentBase);


Object.defineProperty(epfl.ComponentBase.prototype, 'tab_menu', {
    get: function () {
        return $('#' + this.cid + '_tabmenu');
    }
});


epfl.TabsLayout.prototype.after_response = function () {
    var obj = this;
    obj.tab_menu.find('a').click(function (event) {
        event.preventDefault();
        if ($(this).parent().hasClass("active")) {
            return;
        }
        var selected_compo_cid = $(this).data('tab-compo-cid');
        obj.send_event("toggle_tab", {"selected_compo_cid": selected_compo_cid});
    });

    window.setTimeout(function () {
        obj.elm.find('[role="tabpanel"]').addClass("tab-pane");
    }, 0);
};
