$('[epflid=' + '{{ compo.cid }}' + '] > div.panel-body > .fa.fa-lg.fa-edit').click(function () {
    epfl.send(epfl.make_component_event('{{ compo.cid }}', 'edit_note'));
});