<%inherit file="jobinator:templates/sidebar_layout.mako" />

<%def name="content()">
    <h1>Filters</h1>
    <ul>
        % for item in items:
            <li><a href="${request.route_url('filter_list', filter_pk=item.pk)}${item.pk}">${item.name} (view)</a><a href="${request.route_url('filter_edit', filter_pk=item.pk)}">(edit)</a><a href="${request.route_url('filter_list', filter_pk=item.pk)}${item.pk}/remove">(remove)</a></li>
        % endfor
    </ul>
</%def>
