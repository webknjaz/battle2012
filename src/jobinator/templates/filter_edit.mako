<%inherit file="jobinator:templates/filter_form.mako" />

<%def name="form_title()">
    Edit filter <small><a href="${request.route_url('filter_view', filter_pk=request.context.pk)}">(view)</a></small>
</%def>
