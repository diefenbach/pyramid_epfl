epfl.PluginContextMenu = function (selector,cid) {
    var element = $(selector);

    element.parent().mouseleave(function (event) {
        element.hide();
    });

    element.children("li.entry").click(function (event) {
        event.stopPropagation();
        $(this).parent().hide();
        var liEvent = $(this).data("event");
        var liId = $(this).data("id");
        var liData = $(this).data("data");
        epfl.components[cid].send_event(liEvent, {entry_id: liId, data: liData});
    });

    element.parent().find("button").click(function (event) {
        event.stopPropagation();
        var ul = $(this).parent().find("ul");
        if (ul.is(":visible")) {
            ul.hide();
        } else {
            ul.show();
            ul.css({
                top: ($(this).offset().top + $(this).height() + 3) - $(window).scrollTop(),
                left: $(this).offset().left - (ul.width() - $(this).width() - 10)
            })
        }
    });

    $(document).click(function(){
        $("ul.context-dropdown-menu").hide();
    });
};
