$(document).ready(function() {
    var panelBodies = $('.panel-body');
    for(i=0; i<panelBodies.length; i++) {
        var $panelBody = $(panelBodies[i]);
        try {
            var input = eval('(' + $panelBody.find('#errorGetData').val() + ')');
            $panelBody.find('#errorGet').jsonViewer(input, {collapsed: true});

            var input = eval('(' + $panelBody.find('#errorPostData').val() + ')');
            $panelBody.find('#errorPost').jsonViewer(input, {collapsed: true});

            var input = eval('(' + $panelBody.find('#errorCookiesData').val() + ')');
            $panelBody.find('#errorCookies').jsonViewer(input, {collapsed: true});
            debugger;
            var input = eval('(' + $panelBody.find('#errorBodyData').val() + ')');
            $panelBody.find('#errorBody').jsonViewer(input, {collapsed: true});

            var input = eval('(' + $panelBody.find('#errorMetaData').val() + ')');
            $panelBody.find('#errorMeta').jsonViewer(input, {collapsed: true});
        }
        catch (error) {
            alert("Cannot eval JSON: " + error);
        }
    };
});