epfl.Diagram = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.Diagram.inherits_from(epfl.ComponentBase);

epfl.Diagram.prototype.after_response = function () {
    var compo = this;

    this.elm.highcharts(this.params.diagram_params);

    // handle changes in series visibility
    this.elm.find('.highcharts-legend-item').click(function (event) {
        var my_chart = $('#' + cid).highcharts();
        var series_visibility = [];
        for (var i = 0; i < my_chart.series.length; i++) {
            var series = my_chart.series[i];
            var series_json = {"name": series.name};
            if (series.visible == false) {
                series_json["visible"] = false;
            }
            series_visibility.push(series_json);
        }
        compo.send_event("visibilityChange", {series_visibility: series_visibility});
    });
};
