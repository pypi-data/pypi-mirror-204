import re
from . import utils
import sys

REGULAR = 0
BOLD = 1
ITALIC = 2
BOLD_ITALIC = 3

STYLES = {
    'regular': REGULAR,
    'bold': BOLD,
    'italic': ITALIC,
    'bold italic': BOLD_ITALIC
}

# notes for Phoebus:
# - Only supports font size in pixels
# - String as font style

# phoebus font style
STYLE_MAP = {
    REGULAR: 'REGULAR',
    BOLD: 'BOLD',
    ITALIC: 'ITALIC',
    BOLD_ITALIC: 'BOLD_ITALIC',
}


class Font(object):
    """Representation of a font."""

    def __init__(self,
                 name=None,
                 fontface='Liberation Sans',
                 size=15,
                 style=REGULAR,
                 pixels=True,
                 **kws):
        # If the font name is specified, and defined in CS-Studio's fonts.def
        # than this overrides all over attributes.
        # keyword arguments:
        # phoebus_size : font size for phoebus in pixel
        self.fontface = fontface
        self.size = size
        self.style = style
        self.pixels = pixels
        self.name = name
        _phoebus_size = kws.get('phoebus_size', None)
        if _phoebus_size is None:
            _phoebus_size = size
        self.phoebus_size = _phoebus_size

    def __eq__(self, other):
        val = (self.size == other.size
               and self.phoebus_size == other.phoebus_size
               and self.style == other.style and self.pixels == other.pixels)
        return val

    def style_as_str(self) -> str:
        # phoebus font style
        return STYLE_MAP[self.style]

    def __str__(self):
        pixels_or_points = 'px' if self.pixels else 'pt'
        format_string = 'Font name {}: {} style {} ({}) size {}{}'
        return format_string.format(self.name, self.fontface, self.style,
                                    self.style_as_str(), self.size,
                                    pixels_or_points)

    def __repr__(self):
        return str(self)


_pattern = re.compile(
    r'([0-9a-zA-Z ]+)\s*=\s*([a-zA-Z ]+)\s*-\s*([a-zA-Z ]+)\s*-\s*([0-9]+)\s*(.*)'
)


def parse_font_file(filename: str):
    """ Parse the provided font.def file, create Font objects for each
    defined font and attach them to the namespace of this module with
    names converted into appropriate constants by the utils.mangle_name()
    function. By default the font size unit is 'px'.

    Parameters
    ----------
    filename : str
        Filepath of the font definition file.
    """
    with open(filename, "r") as f:
        for line in f.readlines():
            _r = _pattern.match(line.strip())
            if _r is None:
                continue
            _name, _family, _style, _size, _left = _r.groups()

            # font name, all upper cases, ' ' -> '_'
            _font_name = _name.strip()
            _module_name = utils.mangle_name(_font_name)
            # font face or family
            _family = _family.strip()
            # font style
            _style = _style.strip()
            _style_enum = STYLES[_style]
            # font height or size (BOY)
            _size = int(_size)
            # font size in pixel? (BOY only)
            _is_pixel = False if "pt" in _left else True
            _size_bob = re.findall(r'\d+', _left)
            if not _size_bob:
                _size_bob = _size
            else:
                _size_bob = int(_size_bob[0])  # in px

            _f = Font(_font_name,
                      _family,
                      _size,
                      _style_enum,
                      _is_pixel,
                      phoebus_size=_size_bob)
            utils.add_attr_to_module(_module_name, _f, sys.modules[__name__])
