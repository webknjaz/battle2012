<%inherit file="jobinator:templates/app_layout.mako" />

<%def name="body()">
<a href="${request.route_url('horus_admin_users_create')}">Create New User</a>

<ul>
  <li><a href="${request.route_url('horus_admin_users_index')}">User List</a></li>
</ul>
</%def>
