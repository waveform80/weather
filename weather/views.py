from pyramid.view import view_config
from pyramid.response import Response
from weather.anim import WeatherAnimation

@view_config(route_name='index', renderer='templates/index.pt')
def index(request):
    image_query = {}
    if request.params.get('rain'):
        image_query['rain'] = True
    image_query['clouds'] = request.params.get('clouds', 'none')
    return {'image_query': image_query}

@view_config(route_name='test', renderer='templates/mytemplate.pt')
def test(request):
    return {'project': 'weather'}

@view_config(route_name='image')
def image_svg(request):
    anim = WeatherAnimation()
    anim.rain = bool(request.params.get('rain', False))
    anim.clouds = request.params.get('clouds', 'none')
    response = request.response
    response.content_type = 'image/svg+xml'
    response.charset = 'utf-8'
    response.body = str(anim)
    return response
