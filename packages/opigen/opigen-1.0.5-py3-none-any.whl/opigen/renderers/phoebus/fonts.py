import lxml.etree as et


class OpiFont(object):

    def render(self, widget_node, tag_name, font_model):
        font_node = et.SubElement(widget_node, tag_name)
        # opifont_node = et.SubElement(font_node, 'opifont.name')
        opifont_node = et.SubElement(font_node, 'font')
        opifont_node.set('family', font_model.fontface)
        opifont_node.set('size', str(font_model.phoebus_size))
        opifont_node.set('style', font_model.style_as_str())
        # opifont_node.set('pixels', str(font_model.pixels).lower())
        if font_model.name is not None:
            opifont_node.text = str(font_model.name)
