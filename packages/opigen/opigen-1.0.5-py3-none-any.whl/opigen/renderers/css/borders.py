class OpiBorder(object):

    def __init__(self, text_renderer, color_renderer):
        self._text = text_renderer
        self._color = color_renderer

    def render(self, widget_node, _, border_model):
        self._text.render(widget_node, 'border_alarm_sensitive',
                          border_model.alarm)
        self._text.render(widget_node, 'border_width', border_model.width)
        self._text.render(widget_node, 'border_style', border_model.style)
        self._color.render(widget_node, 'border_color', border_model.color)
