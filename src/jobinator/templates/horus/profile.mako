<%inherit file="jobinator:templates/app_layout.mako" />

<%def name="body()">
    <h1>Profile</h1>
    ${ user.username }<br />
    ${ user.email }
</%def>
