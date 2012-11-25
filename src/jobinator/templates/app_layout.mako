<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>${next.title()}</title>

    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Mobile viewport optimisation -->
  <link href="${request.static_url('jobinator:static/img/favicon.ico')}" rel="shortcut icon">
  <link href="${request.static_url('jobinator:static/css/bootstrap.min.css')}" rel="stylesheet">
      <style type="text/css">
      body {
        padding-top: 60px;
        padding-bottom: 40px;
      }
      .sidebar-nav {
        padding: 9px 0;
      }
    </style>
  <link href="${request.static_url('jobinator:static/css/bootstrap-responsive.min.css')}" rel="stylesheet">

  <!-- HTML5, for IE6-8 support of HTML5 elements -->
  <!--[if lt IE 9]>
    <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
  <![endif]-->

  <!-- Touch icons -->
  <link rel="apple-touch-icon-precomposed" sizes="144x144" href="${request.static_url('jobinator:static/img/apple-touch-icon-144-precomposed.png')}">
  <link rel="apple-touch-icon-precomposed" sizes="114x114" href="${request.static_url('jobinator:static/img/apple-touch-icon-114-precomposed.png')}">
  <link rel="apple-touch-icon-precomposed" sizes="72x72" href="${request.static_url('jobinator:static/img/apple-touch-icon-72-precomposed.png')}">
  <link rel="apple-touch-icon-precomposed" href="${request.static_url('jobinator:static/img/apple-touch-icon-57-precomposed.png')}">
  <script type="text/javascript">
    var X_CSRF_TOKEN = '${request.session.get_csrf_token()}';
    % if request.user:
        var USER_ID = ${request.user.pk};
    % endif
  </script>

    <%block name="local_assets_head">
    </%block>

   <link href="${request.static_url('jobinator:static/css/app.css')}" rel="stylesheet">

  </head>
  <body>
    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container${next.layout()}">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="/">Jobinator</a>
          <div class="nav-collapse collapse">
            <p class="navbar-text pull-right">
              % if request.user:
                Logged in as <a href="#" class="navbar-link">${request.user.user_name}</a>
                <a href="${request.route_url('horus_logout')}" class="navbar-link">Log out</a>
              % else:
                <a href="${request.route_url('horus_login')}" class="navbar-link">Log in</a>
                <a href="${request.route_url('horus_register')}" class="navbar-link">Register</a>
              % endif
            </p>
            <ul class="nav">
              <li><a href="/">Home</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container flash">
        % for type in ['success', 'error', 'warning', 'info']:
          % if request.session.peek_flash(type):
            % for message in request.session.pop_flash(type):
              <div class="alert-message ${type}">
                <p><strong>${message}</strong></p>
              </div>
            % endfor
          % endif
        % endfor
    </div>


    <div class="container${next.layout()}">
      ${next.body()}

      <hr/>

      ${next.footer()}

    </div><!--/.container-->

    <script src="${request.static_url('jobinator:static/js/jquery-all-min.js')}"></script>
    <script src="${request.static_url('jobinator:static/js/jquery.jsonrpc.js')}"></script>
    <script src="${request.static_url('jobinator:static/js/bootstrap.min.js')}"></script>
    <script src="${request.static_url('jobinator:static/js/app.js')}"></script>

    <%block name="local_assets_body">
    </%block>

  </body>
</html>

<%def name="title()">
  Home
</%def>

<%def name="footer()">
  <footer>
    <p>&copy; Jobinator Team 2012</p>
    <script type="text/javascript" src="//yandex.st/share/share.js" charset="utf-8"></script>
    <div class="yashare-auto-init" data-yashareL10n="ru" data-yashareType="button" data-yashareQuickServices="yaru,vkontakte,facebook,twitter,gplus"></div> 
  </footer>
</%def>

<%def name="layout()"></%def>
