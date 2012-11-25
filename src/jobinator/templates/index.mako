<%inherit file="jobinator:templates/sidebar_layout.mako" />

<%def name="content()">
          <div class="hero-unit">
            <h1>Jobinator</h1>
            <p>This is a simple job monitoring system. See left menu for possible actions</p>
            %if not request.user:
                <p><a class="btn btn-primary btn-large" href="${request.route_url('horus_login')}">Log in</a></p>
            %endif
          </div>
</%def>

<%def name="title()">
  Home
</%def>
