<%inherit file="jobinator:templates/app_layout.mako" />

<%def name="body()">
% if appstruct:
  ${form.render(appstruct=appstruct)|n}
% else:
  ${form.render()|n}
% endif
</%def>
