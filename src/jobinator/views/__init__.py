from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config

from sqlalchemy.exc import DBAPIError

from ..models import (DBSession,)
from pyramid.security import authenticated_userid
from pyramid.httpexceptions import HTTPSeeOther


@view_config(route_name='index', renderer='jobinator:templates/index.mako')
def index(request):
    return {'project': 'jobinator'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_jobinator_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""


@forbidden_view_config()
def forbidden_view(request):
    if authenticated_userid(request):
        # user is already logged in, they are really forbidden
        return request.context # the forbidden 403 response

    url = request.route_url('login', _query={'came_from': request.path})
    return HTTPSeeOther(url)
