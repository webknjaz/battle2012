<%inherit file="jobinator:templates/app_layout.mako" />

<%def name="body()">
    <h1>Login</h1>
    ${form|n}
    <a href="${request.route_url('horus_forgot_password')}">Forgot Password</a>
</%def>
