import lxml.etree as et


class OpiColor(object):

    def render(self, widget_node, tag_name, color_model):
        parent_color_node = et.SubElement(widget_node, tag_name)
        color_node = et.SubElement(parent_color_node, 'color')
        color_node.set('red', str(color_model.red))
        color_node.set('green', str(color_model.green))
        color_node.set('blue', str(color_model.blue))
        if color_model.name is not None:
            color_node.set('name', color_model.name)
