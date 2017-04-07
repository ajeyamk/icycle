$(document).ready(function() {
    var panelBodies = $('.panel-body');
    for(i=0; i<panelBodies.length; i++) {
        var $panelBody = $(panelBodies[i]);
        try {
            try {
                var input = eval('(' + $panelBody.find('#logGetData').val() + ')');
            } catch(err) {
                var input = {};
            }
            $panelBody.find('#logGet').jsonViewer(input, {collapsed: true});

            try {
                var input = eval('(' + $panelBody.find('#logCookiesData').val() + ')');
            } catch(err) {
                var input = {};
            }
            $panelBody.find('#logCookies').jsonViewer(input, {collapsed: true});

            try {
                var input = eval('(' + $panelBody.find('#logBodyData').val() + ')');
            } catch(err) {
                var input = {};
            }
            $panelBody.find('#logBody').jsonViewer(input, {collapsed: true});

            try {
                var input = eval('(' + $panelBody.find('#logMetaData').val() + ')');
            } catch(err) {
                var input = {};
            }
            $panelBody.find('#logMeta').jsonViewer(input, {collapsed: true});

            try {
                var input = eval('(' + $panelBody.find('#logResponseBodyData').val() + ')');
            } catch(err) {
                var input = {};
            }
            $panelBody.find('#logResponseBody').jsonViewer(input, {collapsed: true});

            try {
                var input = eval('(' + $panelBody.find('#logResponseHeadersData').val() + ')');
            } catch(err) {
                var input = {};
            }
            $panelBody.find('#logResponseHeaders').jsonViewer(input, {collapsed: true});
        }
        catch (log) {
            alert("Cannot eval JSON: " + log);
        }
    };
});