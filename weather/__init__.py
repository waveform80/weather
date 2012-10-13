from pyramid.config import Configurator

__version__ = '0.1'

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('image', '/image.svg')
    config.add_route('test', '/test.html')
    config.scan()
    return config.make_wsgi_app()
