import re
from . import utils
import sys


class Color(object):
    """Representation of a color."""

    def __init__(self, rgb=(0, 0, 0), name=None):
        self.red, self.green, self.blue = rgb
        self.name = name

    def __str__(self):
        return f"Color {self.name}: ({self.red}, {self.green}, {self.blue})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.red == other.red and \
            self.green == other.green and \
            self.blue == other.blue and \
            self.name == other.name


_pattern = re.compile(r'(.*)=\s*(\d+)\D*(\d+)\D*(\d+)')


def parse_color_file(filepath: str):
    """ Parse the provided color.def file, create Color objects for each
    defined color and attach them to the namespace of this module with
    names converted into appropriate constants by the utils.mangle_name()
    function.

    Parameters
    ----------
    filepath : str
        Filepath of the color file
    """
    with open(filepath, "r") as f:
        for line in f.readlines():
            _r = _pattern.match(line.strip())
            if _r is None:
                continue
            _name, _cr, _cg, _cb = _r.groups()
            _color_name = _name.strip()
            _module_name = utils.mangle_name(_color_name)
            utils.add_attr_to_module(
                _module_name, Color((int(_cr), int(_cg), int(_cb)),
                                    _color_name), sys.modules[__name__])
