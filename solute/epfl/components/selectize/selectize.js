epfl.init_component("{{ compo.cid }}", "Selectize", {
    "fire_change_immediately": {{ compo.fire_change_immediately|format_bool }},
    "search_server_side":{{compo.search_server_side|format_bool}},
    "search_text":"{{ compo.search_text }}",
    "input_focus":{{ compo.input_focus | format_bool }}
});

