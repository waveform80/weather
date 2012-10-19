from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
    )

import os
import copy
try:
    from xml.etree.cElementTree import fromstring, tostring
except ImportError:
    from xml.etree.ElementTree import fromstring, tostring

from weather.svg import (
    SVG_XMLNS,
    SVG_ENCODING,
    element_by_id,
    )

# The SVG template doesn't change and is quite large (300k or so), hence we
# read the whole thing once on module initialization and just copy it as
# required
SVG_TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), 'templates', 'image_optimized.svg')
with open(SVG_TEMPLATE_PATH, 'r') as f:
    SVG_TEMPLATE_IMAGE = fromstring(f.read())


class WeatherAnimation(object):
    """A class representing the SVG animation."""

    def __init__(self):
        super(WeatherAnimation, self).__init__()
        self._doc = copy.deepcopy(SVG_TEMPLATE_IMAGE)
        self._layer = element_by_id(self._doc, '{%s}g' % SVG_XMLNS, 'layer1')
        self._clouds = {
            'light':  element_by_id(self._doc, '{%s}path' % SVG_XMLNS, 'cloud-light'),
            'medium': element_by_id(self._doc, '{%s}g' % SVG_XMLNS, 'cloud-medium'),
            'heavy':  element_by_id(self._doc, '{%s}g' % SVG_XMLNS, 'cloud-heavy'),
        }
        self._rain = element_by_id(self._doc, '{%s}path' % SVG_XMLNS, 'rain1')

    def _get_clouds(self):
        for level in ('heavy', 'medium', 'light'):
            if self._clouds[level].attrib.get('display', '') != 'none':
                return level
        return 'none'

    def _set_clouds(self, value):
        for name, elem in self._clouds.items():
            if name == value:
                if 'display' in elem.attrib:
                    del elem.attrib['display']
            else:
                elem.attrib['display'] = 'none'

    clouds = property(
        _get_clouds, _set_clouds, doc="string property represents cloud level "
            "as 'none', 'light', 'medium', or 'heavy'""")

    def _get_rain(self):
        return self._rain.attrib.get('display', '') != 'none'

    def _set_rain(self, value):
        if value:
            if 'display' in self._rain.attrib:
                del self._rain.attrib['display']
        else:
            self._rain.attrib['display'] = 'none'

    rain = property(
        _get_rain, _set_rain, doc="boolean property which enables or disables "
            "animated rain")

    def __str__(self):
        return tostring(self._doc, encoding=SVG_ENCODING)

    def __unicode__(self):
        return str(self).decode(SVG_ENCODING)

