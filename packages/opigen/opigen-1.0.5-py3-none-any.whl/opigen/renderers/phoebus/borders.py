from opigen.opimodel.borders import BorderStyle_GroupBoxStyle_MAP


class OpiBorder(object):

    def __init__(self, text_renderer, color_renderer):
        self._text = text_renderer
        self._color = color_renderer

    def render(self, widget_node, _, border_model):
        w_type = widget_node.get('type')
        if w_type == 'group':
            # support style
            _style = BorderStyle_GroupBoxStyle_MAP.get(border_model.style, 0)
            self._text.render(widget_node, 'style', _style)
            self._color.render(widget_node, 'foreground_color',
                               border_model.color)
        else:
            self._text.render(widget_node, 'border_alarm_sensitive',
                              border_model.alarm)
            self._text.render(widget_node, 'border_width', border_model.width)
            # phoebus does not support border style
            # self._text.render(widget_node, 'border_style', border_model.style)
            self._color.render(widget_node, 'border_color', border_model.color)
