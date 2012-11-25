<%inherit file="jobinator:templates/form_layout.mako" />

<%block name="local_assets_head">
    <link rel="stylesheet" media="screen" type="text/css" href="${request.static_url('jobinator:static/css/theme/jquery.ui.core.css')}" />
    <link rel="stylesheet" media="screen" type="text/css" href="${request.static_url('jobinator:static/css/theme2/jquery-ui-1.8.22.custom.css')}" />
    <link rel="stylesheet" media="screen" type="text/css" href="${request.static_url('jobinator:static/css/theme/jquery.ui.datepicker.css')}" />
    <link rel="stylesheet" media="screen" type="text/css" href="${request.static_url('jobinator:static/css/theme/jquery.ui.dialog.css')}" />
    <link rel="stylesheet" media="screen" type="text/css" href="${request.static_url('jobinator:static/css/theme/easyquery.css')}" />
</%block>

<%block name="local_assets_body">
    <script src="${request.static_url('jobinator:static/js/eq-all-min.js')}"></script>
    <script src="${request.static_url('jobinator:static/js/conditions.js')}"></script>
    <script src="${request.static_url('jobinator:static/js/conditions-init.js')}"></script>
    <script>
        $(function() {
            language('${request.locale_name}');
         });
    </script>
</%block>

<%def name="form_title()">
    ${next.form_title()}
</%def>
