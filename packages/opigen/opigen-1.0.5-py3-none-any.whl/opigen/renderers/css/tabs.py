from lxml import etree as et
from .colors import OpiColor


class OpiTabs(object):
    """Rendering TabbedContainer."""

    def render(self, widget_node, tag_name, tabs_model):
        from opigen.renderers.css.render import get_opi_renderer
        if len(tabs_model) == 0:
            return
        for i, (name, widget, bg_color, fg_color) in enumerate(tabs_model):
            tab_title_node = et.SubElement(widget_node, f"tab_{i}_title")
            tab_title_node.text = name
            for (_c, _attr) in zip((bg_color, fg_color),
                                   ('background_color', 'foreground_color')):
                if _c is None:
                    continue
                OpiColor().render(widget_node, f"tab_{i}_{_attr}", _c)
            _widget_renderer = get_opi_renderer(widget)
            _widget_renderer.assemble()
            _widget_node = _widget_renderer.get_node() # group widget
            widget_node.append(_widget_node)