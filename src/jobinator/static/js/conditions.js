function btnClear() {
    console.log('you click clear button')
}

function btnSave() {
    console.log('you click save button')
}

function language(prop) {
    //console.log('you click the change language to: ' + prop);
    requestUrl = '/static/lng/' + prop + '/querypanel.lng';
    try {
        $.ajax({
            type: "GET",
            url: requestUrl,
            cache: false,
            beforeSend: function (x) {
                if (x && x.overrideMimeType) {
                    x.overrideMimeType("application/j-son;charset=UTF-8");
                }
            },
            dataType: "json",
            success: function (data) {
                EQ.core.texts = data.texts ? data.texts : {};
                $('#QueryPanel').QueryPanel('refresh');
            },
            error: function () {
                EQ.core.texts = {};
                $('#QueryPanel').QueryPanel('refresh');
            }
        });
    }
    catch (e) {
        EQ.core.texts = {};
        $('#QueryPanel').QueryPanel('refresh');
    }

    var locale = prop === 'en' ? '' : prop;
    $.datepicker.setDefaults($.datepicker.regional[locale]);
}

$(document).ready(function () {
    conditionHeight();
});


function conditionHeight() {

}

function DrawGrid(grid) {

    var table = {};
//    var grid = $.parseJSON(jsonText);

    table.body = $('<table></table>').css('width', '100%');

    if (grid.table === undefined) {
        table.body.html('<span class="eqjs-result-error">' + grid.error + '</span>');
        return table.body;
    }

    for (var i = 0; i < grid.table.captions.length; i++) {
        table.captions = '<th>' + grid.table.captions[i] + '</th>';
        table.body.append(table.captions);
    }

    table.body.wrapInner('<tr class="eqjs-result-header"></tr>');


    for (i = 0; i < grid.table.rows.length; i++) {

        var trbody = '';
        for (var j = 0; j < grid.table.rows[i].length; j++) {
            table.td = '<td>' + grid.table.rows[i][j] + '</td>';
            trbody += table.td;
        }

        table.tr = '<tr>' + trbody + '</tr>'

        table.body.append(table.tr);
    }

    return table.body;
}

var loader = $('<div></div>', { 'class': 'eqjs-result loader' });

function GetSQLBeforeSend(blockResult) {
    var sqlPanel = $(blockResult);

    sqlPanel.animate({ opacity: '0.5' }, 200);

    sqlPanel.append(loader.clone())
};

function ExecuteSQLBeforeSend(blockResult) {
    var resultPanel = $(blockResult); //.parentsUntil('#content').eq(1);

    resultPanel.animate({ opacity: '0.5' }, 200);

    resultPanel.html(loader);
};


function GetSQLSuccess(blockSQL, sqlText) {

    try {
        var m = $.parseJSON(sqlText);
        if (m.error != undefined) {
//            $(blockSQL).addClass('error').append('<div class="errorBlock">ERROR: ' + m.error + '</div>');
            $(blockSQL).addClass('error').html('<div class="errorBlock"><div>' + m.error + '</div></div>');
        }
    }
    catch (ex) {
        $(blockSQL).animate({ 'opacity': 1 }, 200);

        $(blockSQL).html('<div class="eqjs-sql-result">' + sqlText + '</div>');

        loader.remove();
    }

};

function ExecuteSQLSuccess(blockResult, gridJson) {

    var resultParent = $(blockResult); //.parentsUntil('#content').eq(1),
    var grid = this.DrawGrid(gridJson);


    $(blockResult).html(grid).delay(100);

    loader.remove();

    resultParent.animate({
        'opacity': 1
    }, 200);


};

function GetSQLError(resultBlock, errorText, errorMsg) {
    $(resultBlock).addClass('error').prepend('<div class="errorBlock">ERROR: ' + errorText + '<div>' + $.parseJSON(errorMsg).Message + '</div></div>');
};

function ExecuteSQLError(resultBlock, errorText, errorMsg) {
    loader.remove();
    $(resultBlock).animate({'opacity': 1}, 200);
    $(resultBlock).addClass('error').append('<div class="errorBlock">ERROR: ' + errorText + '<div>' + $.parseJSON(errorMsg).Message + '</div></div>');
}
