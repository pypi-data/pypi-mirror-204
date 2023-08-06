class GroupBoxBorderStyle:
    # group box border style for phoebus
    GROUP_BOX = 0
    TITLE_BAR = 1
    LINE = 2
    NONE = 3


# phoebus does not support border style.
class BorderStyle:
    NONE = 0
    LINE = 1
    RAISED = 2
    LOWERED = 3
    ETCHED = 4
    RIDGED = 5
    BUTTON_RAISED = 6
    BUTTON_PRESSED = 7
    DOT = 8
    DASH = 9
    DASH_DOT = 10
    DASH_DOT_DOT = 11
    TITLE_BAR = 12
    GROUP_BOX = 13
    ROUND_RECTANGLE_BACKGROUND = 14
    EMPTY = 15


# only for phoebus group widget
BorderStyle_GroupBoxStyle_MAP = {
    BorderStyle.GROUP_BOX: GroupBoxBorderStyle.GROUP_BOX,
    BorderStyle.TITLE_BAR: GroupBoxBorderStyle.TITLE_BAR,
    BorderStyle.LINE: GroupBoxBorderStyle.LINE,
    BorderStyle.NONE: GroupBoxBorderStyle.NONE
}


class Border(object):

    def __init__(self, style, width, color, alarm: bool):
        # style: only applies to BOY
        # alarm refers to 'Alarm Sensitive' in 'Border' section (BOY),
        # and 'Alarm Border' in 'Behavior' section (BOB)
        self.alarm = alarm
        self.color = color
        self.style = style
        self.width = width
