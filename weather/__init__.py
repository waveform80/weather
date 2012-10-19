from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
    )

from pyramid.config import Configurator

__version__ = '0.1'

def main(global_config, **settings):
    """This function returns the WSGI application"""
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('image', '/image.svg')
    config.scan()
    return config.make_wsgi_app()
