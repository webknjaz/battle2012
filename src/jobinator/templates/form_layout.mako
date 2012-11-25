<%inherit file="jobinator:templates/sidebar_layout.mako" />

<%def name="content()">
    <h1>${next.form_title()}</h1>
    % if appstruct:
      ${form.render(appstruct=appstruct)|n}
    % else:
      ${form.render()|n}
    % endif

</%def>
