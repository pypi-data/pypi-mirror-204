class ScaleOptions(object):
    """ Representation of a widget scaling."""

    def __init__(self, width=True, height=True, keep_ratio=False):

        self.width_scalable = width
        self.height_scalable = height
        self.keep_wh_ratio = keep_ratio


class DisplayScaleOptions(object):
    """ Representation of a Display scaling."""

    def __init__(self, min_width=-1, min_height=-1, autoscale=True):

        self.min_width = min_width
        self.min_height = min_height
        self.auto_scale_widgets = autoscale
