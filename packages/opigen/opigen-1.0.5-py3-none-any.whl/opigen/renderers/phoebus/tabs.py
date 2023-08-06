from lxml import etree as et
from .colors import OpiColor


class OpiTabs(object):
    """Rendering TabbedContainer."""

    def render(self, widget_node, tag_name, tabs_model):
        from opigen.renderers.phoebus.render import get_opi_renderer
        if len(tabs_model) == 0:
            return
        tab_root_node = et.SubElement(widget_node, "tabs")
        for name, widget, bg_color, fg_color in tabs_model:
            tab_node = et.SubElement(tab_root_node, "tab")
            tab_name_node = et.SubElement(tab_node, "name")
            tab_name_node.text = name
            for (_c, _attr) in zip((bg_color, fg_color),
                                   ('background_color', 'foreground_color')):
                if _c is None:
                    continue
                OpiColor().render(tab_node, _attr, _c)
            child_node = et.SubElement(tab_node, "children")
            _widget_renderer = get_opi_renderer(widget)
            _widget_renderer.assemble()
            _widget_node = _widget_renderer.get_node()
            child_node.append(_widget_node)