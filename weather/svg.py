from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
    )

from collections import namedtuple


SVG_XMLNS = 'http://www.w3.org/2000/svg'
SVG_ENCODING = 'utf-8'


def rgb_to_hex(rgb):
    "Convert an (R, G, B) tuple to #RRGGBB"
    return '#%02x%02x%02x' % rgb

def hex_to_rgb(s):
    "Convert #RRGGBB to an (R, G, B) tuple"
    if s[:1] == '#':
        s = s[1:]
    if len(s) != 6:
        raise ValueError, "input %s is not in #RRGGBB format" % s
    return tuple(int(s[i:i + 2], 16) for i in range(0, len(s), 2))

def element_by_id(root, tag, id):
    "Find the tag element with id under root"
    for elem in root.getiterator(tag):
        if elem.attrib.get('id') == id:
            return elem
    raise ValueError(
        'Unable to locate a %s element with id %s under root' % (tag, id))

def style_to_dict(style):
    "Construct a dictionary from an SVG style attribute"
    return dict(s.split(':', 1) for s in style.split(';'))

def dict_to_style(style):
    "Consrtuct an SVG style attribute from a dictionary"
    return ';'.join('%s:%s' % (name, value) for (name, value) in style.items())

def transform_to_sequence(transform):
    "Parse a transform attribute into a sequence of Transformation objects"
    # XXX pyparsing?
    raise NotImplementedError

def sequence_to_transform(transforms):
    "Construct a transform attribute from a sequence of Transformation objects"
    return ' '.join(str(transform) for transform in transforms)


Coord = namedtuple('Coord', ('x', 'y'))


class Transformation(object):
    "Base class for SVG transform clauses"


class Translate(Transformation):
    "Represents a translate() clause in an SVG transform attribute"

    def __init__(self, x, y=0):
        self.x = float(x)
        self.y = float(y)

    def inverse(self):
        return Translate(-self.x, -self.y)

    def __str__(self):
        return 'translate(%f,%f)' % (self.x, self.y)


class Scale(Transformation):
    "Represents a scale() clause in an SVG transform attribute"

    def __init__(self, x, y=None):
        self.x = float(x)
        if y is None:
            self.y = x
        else:
            self.y = float(y)

    def inverse(self):
        return Scale(1.0 / self.x, 1.0 / self.y)

    def __str__(self):
        return 'scale(%f,%f)' % (self.x, self.y)


class Rotate(Transformation):
    "Represents a rotate() clause in an SVG transform attribute"

    def __init__(self, degrees, origin=None):
        self.degrees = float(degrees)
        if origin is None:
            self.origin = None
        else:
            self.origin = Coord(*origin)

    def inverse(self):
        return Rotate(-self.degrees, self.origin)

    def __str__(self):
        if self.origin:
            return 'rotate(%f,%f,%f)' % (
                self.degrees, self.origin.x, self.origin.y)
        else:
            return 'rotate(%f)' % self.degrees

