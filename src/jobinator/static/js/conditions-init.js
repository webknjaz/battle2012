$(document).ready(function () {

    $.jsonRPC.setup({
        endPoint: '/api/filter'
      });

    var QueryPanelBlock = $('#QueryPanel'),
        menuContent = $('.eqJsMenuBlock_content'),
        mw = QueryPanelBlock.QueryPanel();

    $.jsonRPC.request('get_model', {
        success: function(result) {
            QueryPanelBlock.QueryPanel('option', 'model', result.result);
            if ($('input[name=filter_details]').val()) {
                QueryPanelBlock.QueryPanel('option', 'query', $.parseJSON($('input[name=filter_details]').val()));
            }
         }
      });

    $('input[name=filter_details]').parents('form').submit(function() {
        var q = QueryPanelBlock.QueryPanel('option', 'query');
        var str = $.toJSON(q);
        $('input[name=filter_details]').val(str)
    })
});
