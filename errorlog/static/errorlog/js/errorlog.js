$(document).ready(function() {
    var panelBodies = $('.panel-body');
    for(i=0; i<panelBodies.length; i++) {
        var $panelBody = $(panelBodies[i]);
        try {
            try {
                var input = eval('(' + $panelBody.find('#errorGetData').val() + ')');
            } catch(err) {
                var input = {};
            }
            $panelBody.find('#errorGet').jsonViewer(input, {collapsed: true});

            try {
                var input = eval('(' + $panelBody.find('#errorPostData').val() + ')');
            } catch(err) {
                var input = {};
            }
            $panelBody.find('#errorPost').jsonViewer(input, {collapsed: true});

            try {
                var input = eval('(' + $panelBody.find('#errorCookiesData').val() + ')');
            } catch(err) {
                var input = {};
            }
            $panelBody.find('#errorCookies').jsonViewer(input, {collapsed: true});

            try {
                var input = eval('(' + $panelBody.find('#errorBodyData').val() + ')');
            } catch(err) {
                var input = {};
            }
            $panelBody.find('#errorBody').jsonViewer(input, {collapsed: true});

            try {
                var input = eval('(' + $panelBody.find('#errorMetaData').val() + ')');
            } catch(err) {
                var input = {};
            }
            $panelBody.find('#errorMeta').jsonViewer(input, {collapsed: true});
        }
        catch (error) {
            alert("Cannot eval JSON: " + error);
        }
    };
});