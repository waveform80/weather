from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
    )

from pyramid.view import view_config
from pyramid.response import Response
from weather.anim import WeatherAnimation
from weather.svg import SVG_ENCODING

@view_config(route_name='index', renderer='templates/index.pt')
def index(request):
    image_query = {}
    if request.params.get('rain'):
        image_query['rain'] = True
    image_query['clouds'] = request.params.get('clouds', 'none')
    return {'image_query': image_query}

@view_config(route_name='image')
def image_svg(request):
    anim = WeatherAnimation()
    anim.rain = bool(request.params.get('rain', False))
    anim.clouds = request.params.get('clouds', 'none')
    response = request.response
    # Headers can't be specified as unicode strings (why?!)
    response.content_type = 'image/svg+xml'.encode('ascii')
    response.charset = SVG_ENCODING.encode('ascii')
    response.body = str(anim)
    return response
