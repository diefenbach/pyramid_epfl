$(function () {
    epfl.init_component("{{compo.cid}}", "TreeLayoutComponent",
    					{ "label": "{{ compo.label }}", "show_context_menu_on_hover_only": {{ compo.show_context_menu_on_hover_only|format_bool }} });
});