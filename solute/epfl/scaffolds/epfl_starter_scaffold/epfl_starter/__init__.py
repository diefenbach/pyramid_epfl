# * coding: utf-8

from pyramid.config import Configurator

from pyramid_beaker import session_factory_from_settings

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from solute.epfl import epfltempdata


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include("solute.epfl")

    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    config.add_static_view(name='static',
                           path='epfl_pyramid_barebone:static',
                           cache_max_age=3600)

    authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    temp_data_provider = epfltempdata.LocalMemoryProvider(config)
    config.set_tempdata_provider(temp_data_provider)

    nodeglobal_data_provider = epfltempdata.LocalMemoryProvider(config)
    config.set_nodeglobaldata_provider(nodeglobal_data_provider)

    config.scan()
    return config.make_wsgi_app()
