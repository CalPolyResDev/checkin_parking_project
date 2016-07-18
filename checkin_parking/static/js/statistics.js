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


function displayChart(jquerySelector, datasourceURL) {    
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
                    text: null
                }
            },
            credits: {
                enabled: false
            },
            series: response.data,
        });
    });
}