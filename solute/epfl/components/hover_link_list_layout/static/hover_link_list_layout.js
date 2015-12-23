epfl.HoverLinkListLayout = function(cid, params) {
    epfl.PaginatedListLayout.call(this, cid, params);
};
// cause LinkListLayout has no JS, so it is no new style, so we use PaginatedListLayout here
epfl.HoverLinkListLayout.inherits_from(epfl.PaginatedListLayout);

epfl.HoverLinkListLayout.prototype.after_response = function(data) {
    epfl.PaginatedListLayout.prototype.after_response.call(this, data);

    var compo = this;

    compo.elm.find('.hover-data-container').hover(
        function(e) {
            $('<div id="hover_element'+$(this).parent().attr('epflid')+'">')
                .css('position', 'absolute')
                .css('top', e.pageY + 'px')
                .css('left', (e.pageX + 10) + 'px')
                .css('z-index', '100')
                .append('<img src="'+$(this).data('src')+'" class="img-thumbnail" />')
                .appendTo(document.body);
        }, function(e) {
            $('#hover_element'+$(this).parent().attr('epflid')).remove();
        })
        .click(function(e) {
            $('#hover_element'+$(this).parent().attr('epflid')).remove();
        });
};
