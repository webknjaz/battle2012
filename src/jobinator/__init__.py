from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config

from .models import DBSession, User, Activation
from jobinator.models import initialize_sql
from pyramid.interfaces import IAuthorizationPolicy, IAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from horus import groupfinder


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""

    engine = engine_from_config(settings, 'sqlalchemy.')
    session_factory = session_factory_from_settings(settings)
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings, session_factory=session_factory)

    if not config.registry.queryUtility(IAuthorizationPolicy):
        authz_policy = ACLAuthorizationPolicy()
        config.set_authorization_policy(authz_policy)

    if not config.registry.queryUtility(IAuthenticationPolicy):
        authn_policy = AuthTktAuthenticationPolicy(
            settings.get('jobinator.auth_secret'),
            callback=groupfinder)
        config.set_authentication_policy(authn_policy)

    # Include horus
    from hem.interfaces import IDBSession
    from horus.interfaces import IHorusUserClass, IHorusActivationClass
    # Tell horus which SQLAlchemy session to use:
    config.registry.registerUtility(DBSession, IDBSession)
    config.registry.registerUtility(User, IHorusUserClass)
    config.registry.registerUtility(Activation, IHorusActivationClass)
    config.include('horus', route_prefix='auth')
    config.include('pyramid_rpc.jsonrpc')
    #config.include('hiero', route_prefix='hiero')

    config.include('pyramid_mailer')

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.include('jobinator.routes')

    config.override_asset(to_override='horus:templates/',
                          override_with='jobinator:templates/horus/')
    config.scan()

    initialize_sql(engine)

    return config.make_wsgi_app()
