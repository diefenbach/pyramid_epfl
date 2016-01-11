# * coding: utf-8

from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings


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

    config.scan()
    return config.make_wsgi_app()
