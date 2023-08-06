__version__ = "1.0.5"

from .opimodel import actions
from .opimodel import borders
from .opimodel import colors
from .opimodel import fonts
from .opimodel import rules
from .opimodel import widgets

from .renderers import *

from .config import get_color_def_path
from .config import get_font_def_path

# load font def
fonts.parse_font_file(get_font_def_path())
# load color def
colors.parse_color_file(get_color_def_path())
