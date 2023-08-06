"""
Module containing widgets to describe opi files.  An opi has a root widget
of type Display.  To create the opi, add widgets as children of this widget.
"""
from . import actions, scalings
from .colors import Color
from .borders import Border, BorderStyle
from opigen.config import get_attr_conf

ATTR_MAP = get_attr_conf()


class ResizeBehaviour:
    # for LinkingContainer (BOY)
    RESIZE_OPI_TO_FIT_CONTAINER = 0  # Size *.opi to fit the container
    RESIZE_CONTAINER_TO_FIT_OPI = 1  # Size the container to fit *.opi
    CROP = 2  # Don't resize anything, crop if *.opi too large
    SCROLL = 3  # Don't resize anything, add scrollbars if *.opi too large


class ResizeBehaviour_Embeded:
    # for embeded display (Phoebus)
    NO_RESIZE = 0  # no resize, add scroll if needed
    RESIZE_OPI_TO_FIT_CONTAINER = 1  # Size content to fit widget
    RESIZE_CONTAINER_TO_FIT_OPI = 2  # Size widget to match content
    STRETCH_OPI_TO_FIT_CONTAINER = 3  # Stretch content to fit widget
    CROP = 4  # Crop content


ResizeBehaviour_MAP = {
    ResizeBehaviour.RESIZE_OPI_TO_FIT_CONTAINER:
    ResizeBehaviour_Embeded.RESIZE_OPI_TO_FIT_CONTAINER,
    ResizeBehaviour.RESIZE_CONTAINER_TO_FIT_OPI:
    ResizeBehaviour_Embeded.RESIZE_CONTAINER_TO_FIT_OPI,
    ResizeBehaviour.CROP: ResizeBehaviour_Embeded.CROP,
    ResizeBehaviour.SCROLL: ResizeBehaviour_Embeded.NO_RESIZE,
}


class FormatType:
    DEFAULT = 0
    DECIMAL = 1
    EXPONENTIAL = 2
    HEX_32 = 3
    STRING = 4
    HEX_64 = 5
    COMPACT = 6
    ENGINEERING = 7
    SEXAGESIMAL = 8
    SEXAGESIMAL_HMS = 9
    SEXAGESIMAL_DMS = 10


class FormatType_PHOEBUS:
    DEFAULT = 0
    DECIMAL = 1
    EXPONENTIAL = 2
    ENGINEERING = 3
    HEXADECIMAL = 4
    COMPACT = 5
    STRING = 6
    SEXAGESIMAL = 7
    SEXAGESIMAL_HMS = 8
    SEXAGESIMAL_DMS = 9


# for phoebus (BOY to BOB)
FormatType_MAP = {
    FormatType.DEFAULT: FormatType_PHOEBUS.DEFAULT,
    FormatType.DECIMAL: FormatType_PHOEBUS.DECIMAL,
    FormatType.EXPONENTIAL: FormatType_PHOEBUS.EXPONENTIAL,
    FormatType.HEX_32: FormatType_PHOEBUS.HEXADECIMAL,
    FormatType.STRING: FormatType_PHOEBUS.STRING,
    FormatType.HEX_64: FormatType_PHOEBUS.HEXADECIMAL,
    FormatType.COMPACT: FormatType_PHOEBUS.COMPACT,
    FormatType.ENGINEERING: FormatType_PHOEBUS.ENGINEERING,
    FormatType.SEXAGESIMAL: FormatType_PHOEBUS.SEXAGESIMAL,
    FormatType.SEXAGESIMAL_HMS: FormatType_PHOEBUS.SEXAGESIMAL_HMS,
    FormatType.SEXAGESIMAL_DMS: FormatType_PHOEBUS.SEXAGESIMAL_DMS,
}


# tab direction map (BOY to BOB)
TAB_HORIZONTAL_MAP = {
    True: 0,
    False: 1
}


class BasicStyle:
    # ActionButton, TextEntry
    CLASSIC = 0
    NATIVE = 1


class HAlign:
    """Enum describing horizontal alignment

    This is typically used with the horizontal_alignment property.
    """
    LEFT = 0
    CENTER = 1
    RIGHT = 2


class VAlign:
    """Enum describing vertical alignment

    This is typically used with the vertical_alignment property.
    """
    TOP = 0
    MIDDLE = 1
    BOTTOM = 2


HA_RIGHT = HAlign.RIGHT
HA_CENTER = HAlign.CENTER
HA_LEFT = HAlign.LEFT
VA_TOP = VAlign.TOP
VA_MIDDLE = VAlign.MIDDLE
VA_BOTTOM = VAlign.BOTTOM


class LineStyle:
    SOLID = 0
    DASH = 1
    DOT = 2
    DASHDOT = 3
    DASHDOTDOT = 4


class Widget(object):
    """Base class for any widget to extend.

    Args:
        id - the CSS id for the widget.
        x - the x position of the widget in pixels
        y - the y position of the widget in pixels
        widget - the width of the widget in pixels
        height - the height of the widget in pixels
        name - a name for the widget within the display
    """
    CNT = {}

    def __init__(self, type_id, x, y, width, height, name=None):
        if name is None:
            k = self.__class__.__name__
            v = Widget.CNT.setdefault(k, 0)
            self.name = f"{k}_{v}"
            Widget.CNT[k] += 1
        else:
            self.name = name
        #
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._children = []
        self._parent = None
        self._type_id = type_id
        self.rules = []
        self.phoebus_rules = []

    def __setattr__(self, name, value):
        _cls_name = self.__class__.__name__
        _conf_default = ATTR_MAP['DEFAULT']
        if _cls_name in ATTR_MAP:
            _conf = {k: v for k, v in _conf_default.items()}
            _conf_ = ATTR_MAP.get(_cls_name)
            _conf.update(_conf_)
        else:
            _conf = _conf_default

        if name in _conf:
            super().__setattr__(name, value)
            if name == 'format_type':
                super().__setattr__(f"phoebus_{_conf[name]}",
                                    FormatType_MAP[value])
            elif _cls_name == 'EmbeddedContainer' and name == 'resize_behaviour':
                super().__setattr__(f"phoebus_{_conf[name]}",
                                    ResizeBehaviour_MAP[value])
            elif _cls_name == 'TabbedContainer' and name == 'horizontal_tabs':
                super().__setattr__(f"phoebus_{_conf[name]}",
                                    TAB_HORIZONTAL_MAP[value])
            else:
                super().__setattr__(f"phoebus_{_conf[name]}", value)
        else:
            super().__setattr__(name, value)

    def get_type_name(self):
        # widget type name, i.e. tag name, followed by a real type string ('label') and other attributes.
        return "widget"

    def get_type_id(self):
        return self._type_id

    def get_version(self):
        # css
        return "1.0.0"

    def get_version_phoebus(self):
        # phoebus
        return "2.0.0"

    def get_type(self):
        try:
            return self.TYPE  # phoebus
        except AttributeError:
            return self.get_type_id()  # css

    def get_parent(self):
        """Get the parent widget of this widget.
        """
        return self._parent

    def set_parent(self, parent):
        """Set the parent widget of this widget.

        Args:
            widget to be this widget's parent
        """
        self._parent = parent

    def add_child(self, child):
        """Add a widget as a child of this widget.

        Args:
            child widget
        """
        self._children.append(child)
        child.set_parent(self)

    def add_children(self, children):
        """Add multiple widgets as children of this widget.

        Args:
            sequence of child widgets
        """
        for child in children:
            self.add_child(child)

    def get_children(self):
        """Get all child widgets.
        """
        return self._children

    def set_bg_color(self, color):
        """Set background color for the widget.

        Args:
            Color object
        """
        self.background_color = color

    def set_fg_color(self, color):
        """Set background color for the widget.

        Args:
            Color object
        """
        self.foreground_color = color

    def set_border(self, border):
        """Set border for the widget.

        Args:
            Border object
        """
        self.border = border
        self.phoebus_border = border

    def set_font(self, font):
        """Set font for the widget.

        Args:
            Font object
        """
        self.font = font
        self.phoebus_font = font

    def add_rule(self, rule):
        """Add a rule to the widget.

        Args:
            Rule object
        """
        self.rules.append(rule)
        self.phoebus_rules.append(rule)

    def add_scale_options(self, width=True, height=True, keep_wh_ratio=False):
        """Add scale options to the widget.

        Args:
            width (bool): True if widget width is scalable
            height (bool): True if widget height is scalable
            keep_wh_ratio (bool):
        """
        self.scale_options = scalings.ScaleOptions(width, height,
                                                   keep_wh_ratio)

    def get_resources(self):
        """Return a dict of required resources that need to be distributed with the generated OPI.
        the key is the full path of resource files, and the value is the target path.
        """
        return {}


class ActionWidget(Widget):
    """
    Base class for any widget that can have a list of actions.
    """

    # No ID, designed to be subclassed only
    def __init__(self,
                 type_id,
                 x,
                 y,
                 width,
                 height,
                 hook_first=True,
                 hook_all=False):
        super(ActionWidget, self).__init__(type_id, x, y, width, height)
        self.actions = actions.ActionsModel(hook_first, hook_all)
        self.phoebus_actions = self.actions

    def add_action(self, action):
        """
        Add any action to the list of actions.

        Args:
            action to add
        """
        self.actions.add_action(action)

    def add_write_pv(self, pv, value, description=""):
        self.actions.add_action(actions.WritePv(pv, value, description))

    def add_shell_command(self,
                          command,
                          description="",
                          directory="$(opi.dir)"):
        # directory does not apply to phoebus
        self.actions.add_action(
            actions.ExecuteCommand(command, description, directory))

    def add_open_opi(self,
                     path,
                     mode=actions.OpenOpi.STANDALONE,
                     description=None,
                     macros=None,
                     parent_macros=True):
        self.actions.add_action(
            actions.OpenOpi(path, mode, description, macros, parent_macros))

    def add_exit(self):
        self.actions.add_action(actions.Exit())

    def set_basic_style(self, style):
        # does not work well
        if style == BasicStyle.CLASSIC:
            self.alarm_pulsing = False
            self.backcolor_alarm_sensitive = False
            self.set_bg_color(
                Color((218, 218, 218), 'ControlAndButtons Background'))
            self.style = style
        else:  # NATIVE
            self.style = style


class Display(Widget):
    """
    Display widget.  This is the root widget for any opi.
    """

    TYPE_ID = 'org.csstudio.opibuilder.Display'
    TYPE = None

    def __init__(self, width=800, height=600):
        super(Display, self).__init__(Display.TYPE_ID,
                                      0,
                                      0,
                                      width,
                                      height,
                                      name='display')
        self.auto_zoom_to_fit_all = False
        self.show_grid = True

    def get_type_name(self):
        return "display"

    def add_scale_options(self, min_width=-1, min_height=-1, autoscale=False):
        """Add scale options to the display.

        Args:
            min_width (int): Display min width, -1 for no scaling
            min_height (int): Display min height, -1 for no scaling
            autoscale (bool): Autoscale child widgets
        """
        self.auto_scale_widgets = scalings.DisplayScaleOptions(
            min_width, min_height, autoscale)


class Rectangle(ActionWidget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.Rectangle'
    TYPE = 'rectangle'  # phoebus

    def __init__(self, x, y, width, height):
        super(Rectangle, self).__init__(Rectangle.TYPE_ID, x, y, width, height)


class Line(Widget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.polyline'
    TYPE = 'polyline'

    def __init__(self,
                 x0,
                 y0,
                 x1,
                 y1,
                 line_width=1,
                 line_style=LineStyle.SOLID):
        """ Widget x,y location is calculated to be the top-left corner of
            rectangle defined by the diagonal from (x0, y0) to (x1, y1).
            The width and height are the lengths of the sides.
        """
        super(Line, self).__init__(Line.TYPE_ID,
                                   x=min(x0, x1),
                                   y=min(y0, y1),
                                   width=abs(x0 - x1) + 1,
                                   height=abs(y0 - y1) + 1)
        self.points = [(x0, y0), (x1, y1)]
        self.phoebus_points = [(x0 - self.x, y0 - self.y),
                               (x1 - self.x, y1 - self.y)]
        self.line_width = line_width
        self.line_style = line_style
        self.set_line_color()

    def add_point(self, x, y):
        """Add a point with x, y coordinate."""
        self.points.append((x, y))
        self.phoebus_points.append((x - self.x, y - self.y))

    def set_line_color(self, c: Color = None):
        """Set the line color."""
        if c is None:
            c = Color((189, 195, 199), 'Silver')
        # background_color
        self.set_bg_color(c)


class Label(Widget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.Label'
    TYPE = 'label'  # phoebus

    def __init__(self, x, y, width, height, text):
        super(Label, self).__init__(Label.TYPE_ID, x, y, width, height)
        self.text = text
        self.horizontal_alignment = HAlign.LEFT
        self.vertical_alignment = VAlign.MIDDLE


class TextUpdate(Widget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.TextUpdate'
    TYPE = 'textupdate'

    def __init__(self, x, y, width, height, pv):
        super(TextUpdate, self).__init__(TextUpdate.TYPE_ID, x, y, width,
                                         height)

        self.pv_name = pv
        self.horizontal_alignment = HAlign.CENTER
        self.vertical_alignment = VAlign.MIDDLE


class TextEntry(Widget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.TextInput'
    TYPE = 'textentry'

    def __init__(self, x, y, width, height, pv, style=None):
        super(TextEntry, self).__init__(TextEntry.TYPE_ID, x, y, width, height)

        self.pv_name = pv
        self.horizontal_alignment = HAlign.LEFT
        self.vertical_alignment = VAlign.MIDDLE
        #
        if style is not None:
            self.set_basic_style(style)


class GroupingContainer(Widget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.groupingContainer'
    TYPE = 'group'

    def __init__(self, x, y, width, height, name=''):
        super(GroupingContainer, self).__init__(GroupingContainer.TYPE_ID, x,
                                                y, width, height, name)
        self.lock_children = True
        self.transparent = True  # transparent background


class TabbedContainer(Widget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.tab'
    TYPE = 'tabs'

    def __init__(self, x, y, width, height):
        super(TabbedContainer, self).__init__(TabbedContainer.TYPE_ID, x, y,
                                              width, height)
        self.tab_count = 0
        self.tabs = []
        self.phoebus_tabs = self.tabs

    def add_tab(self,
                name,
                widget,
                dw=2,
                dh=33,
                background_color=None,
                foreground_color=None):
        """Add a new tab named as *name*, embbed with *widget*.

        _grp.width = self.width - dw
        _grp.height = self.height - dh
        """
        # create a grouping container for the content widget
        _grp = GroupingContainer(1, 1, self.width - dw, self.height - dh)
        _grp.add_child(widget)
        _grp.set_border(Border(BorderStyle.NONE, 0, Color((255, 255, 255)), False))
        _grp.name = name
        self.tabs.append((name, _grp, background_color, foreground_color))
        self.tab_count += 1

    def set_font(self, font):
        """Set font for each tab. Call this method after added all tabs (only for BOY).
        """
        self.phoebus_font = font
        for i in range(self.tab_count):
            setattr(self, f"tab_{i}_font", font)


class EmbeddedContainer(Widget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.linkingContainer'
    TYPE = 'embedded'

    def __init__(self, x, y, width, height, opi_file):
        super(EmbeddedContainer, self).__init__(EmbeddedContainer.TYPE_ID, x,
                                                y, width, height)
        self.opi_file = opi_file
        self.resize_behaviour = ResizeBehaviour.CROP


class ActionButton(ActionWidget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.ActionButton'
    TYPE = 'action_button'

    def __init__(self,
                 x,
                 y,
                 width,
                 height,
                 text,
                 style=None,
                 hook_first=True,
                 hook_all=False):
        super(ActionButton, self).__init__(ActionButton.TYPE_ID, x, y, width,
                                           height, hook_first, hook_all)

        self.text = text
        if style is not None:
            self.set_basic_style(style)


class MenuButton(ActionWidget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.MenuButton'

    def __init__(self, x, y, width, height, text):
        super(MenuButton, self).__init__(MenuButton.TYPE_ID, x, y, width,
                                         height)

        self.label = text


class CheckBox(ActionWidget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.checkbox'

    def __init__(self, x, y, width, height, text, pv_name):
        super(CheckBox, self).__init__(CheckBox.TYPE_ID, x, y, width, height)

        self.label = text
        self.pv_name = pv_name


class ToggleButton(ActionWidget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.BoolButton'
    TYPE = 'bool_button'

    def __init__(self, x, y, width, height, on_text, off_text, pv_name=None):
        super(ToggleButton, self).__init__(ToggleButton.TYPE_ID, x, y, width,
                                           height)

        if pv_name is not None:
            self.pv_name = pv_name

        self.on_label = on_text
        self.off_label = off_text
        self.toggle_button = True
        self.effect_3d = True
        self.square_button = True
        self.show_boolean_label = True
        self.show_led = False
        self.push_action_index = 0
        self.released_action_index = 1

    def add_push_action(self, action):
        self.actions.add_action(action)
        self.push_action_index = len(self.actions) - 1

    def add_release_action(self, action):
        self.actions.add_action(action)
        self.released_action_index = len(self.actions) - 1


class Led(Widget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.LED'
    TYPE = 'led'

    def __init__(self, x, y, width, height, pv):
        super(Led, self).__init__(Led.TYPE_ID, x, y, width, height)
        self.pv_name = pv


class Byte(Widget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.bytemonitor'
    TYPE = 'byte_monitor'

    def __init__(self, x, y, width, height, pv, bits, start_bit=None):
        super(Byte, self).__init__(Byte.TYPE_ID, x, y, width, height)
        self.pv_name = pv
        self.effect_3d = False
        self.square_led = False
        self.numBits = bits
        self.led_border = 1
        self.border_alarm_sensitive = False
        self.led_packed = True
        if start_bit is not None:
            self.startBit = start_bit


class Symbol(ActionWidget):
    TYPE_ID = 'org.csstudio.opibuilder.widgets.edm.symbolwidget'

    def __init__(self,
                 x,
                 y,
                 width,
                 height,
                 pv,
                 image_file,
                 image_width,
                 image_index=0):
        super(Symbol, self).__init__(Symbol.TYPE_ID, x, y, width, height)
        self.pv_name = pv
        self.image_file = image_file
        self.image_index = image_index
        self.sub_image_width = image_width


# Tank
class Tank(Widget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.tank'

    def __init__(self, x, y, width, height, pv):
        super(Tank, self).__init__(Tank.TYPE_ID, x, y, width, height)
        self.pv_name = pv
        self.effect_3d = False


class DataBrowser(Widget):

    TYPE_ID = 'org.csstudio.trends.databrowser.opiwidget'

    def __init__(self, x, y, width, height, filename):
        super(DataBrowser, self).__init__(DataBrowser.TYPE_ID, x, y, width,
                                          height)
        self.filename = filename


class ImageBoolButton(ActionWidget):

    TYPE_ID = 'org.csstudio.opibuilder.widgets.ImageBoolButton'

    def __init__(self,
                 x,
                 y,
                 width,
                 height,
                 pv_name=None,
                 on_image=None,
                 off_image=None):
        super(ImageBoolButton, self).__init__(ImageBoolButton.TYPE_ID, x, y,
                                              width, height)
        if on_image is not None:
            self.on_image = on_image
        if off_image is not None:
            self.off_image = off_image
        if pv_name is not None:
            self.pv_name = pv_name


class SlideButton(ActionWidget):

    TYPE_ID = None  # not available for BOY
    TYPE = 'slide_button'

    def __init__(self, x, y, width, height, pv_name=None):
        super(SlideButton, self).__init__(SlideButton.TYPE_ID, x, y, width,
                                          height)
        if pv_name is not None:
            self.phoebus_pv_name = pv_name
        self.phoebus_label = ''