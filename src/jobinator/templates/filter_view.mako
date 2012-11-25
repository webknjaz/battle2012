<%inherit file="jobinator:templates/sidebar_layout.mako" />

<%def name="content()">
    <h1>Filter '${filter}'<small><a href="${request.route_url('filter_edit', filter_pk=request.context.pk)}">(edit)</a></small></h1>
    % if page.items:
        <ul>
            % for item in page.items:
                <li><a target="blank_" href="${item.scraped_data.url}" title="${item.scraped_data.title}">${item.scraped_data.preview|n,striptags}...</a></li>
            % endfor
        </ul>
        ${page.pager('$link_previous ~3~ $link_next [$item_count items found] (Page $page of $page_count)')}
    % else:
        No matching results
    % endif
</%def>
