// Python-Style string formatting
// Source: http://stackoverflow.com/a/18234317
if (!String.prototype.format) {
    String.prototype.format = function() {
        var str = this.toString();
        if (!arguments.length)
            return str;
        var args = typeof arguments[0],
            args = (("string" == args || "number" == args) ? arguments : arguments[0]);
        for (arg in args)
            str = str.replace(RegExp("\\{" + arg + "\\}", "gi"), args[arg]);
        return str;
    }
}

function refreshCharts() {
    var urlArgs = {
        date: $('#use-custom-date').prop('checked') ? $('#custom-display-date').val() : '',
        show_remaining: $('#show-remaining').prop('checked') ? 'True' : 'False'
    };

    displayChart('#zone_chart', DjangoReverse['statistics:zone_chart_data'](urlArgs));
    displayChart('#class_level_chart', DjangoReverse['statistics:class_level_chart_data'](urlArgs));
    displayChart('#residency_chart', DjangoReverse['statistics:residency_chart_data'](urlArgs));
}


function displayChart(jquerySelector, datasourceURL) {
    $(jquerySelector).html('<p style="text-align: center;">Loading... <img style="height: 10px; width: 10px;" src="' + spinnerURL + '"></img></p>');
     
    $.get(datasourceURL, function(response) {   
        $(jquerySelector).html('');
        $(jquerySelector).highcharts({
            chart: {
                type: 'spline',
                backgroundColor: null,
            },
            title: {
                text: null
            },
            xAxis: {
                type: 'datetime',
                title: {
                    text: null
                }
            },
            yAxis: {
                title: {
                    text: 'Reservation Count'
                }
            },
            credits: {
                enabled: false
            },
            series: response.data,
        });
    });
}