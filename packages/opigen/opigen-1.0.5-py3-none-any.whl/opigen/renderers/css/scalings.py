import lxml.etree as et


class OpiScaling(object):

    def __init__(self, text_renderer):
        self._text = text_renderer

    def render(self, widget_node, _, scaling_model):

        scale_node = et.SubElement(widget_node, 'scale_options')
        self._text.render(scale_node, 'width_scalable',
                          scaling_model.width_scalable)
        self._text.render(scale_node, 'height_scalable',
                          scaling_model.height_scalable)
        self._text.render(scale_node, 'keep_wh_ratio',
                          scaling_model.keep_wh_ratio)


class OpiDisplayScaling(object):

    def __init__(self, text_renderer):
        self._text = text_renderer

    def render(self, widget_node, _, scaling_model):
        scale_node = et.SubElement(widget_node, 'auto_scale_widgets')
        self._text.render(scale_node, 'min_width', scaling_model.min_width)
        self._text.render(scale_node, 'min_height', scaling_model.min_height)
        self._text.render(scale_node, 'auto_scale_widgets',
                          scaling_model.auto_scale_widgets)
