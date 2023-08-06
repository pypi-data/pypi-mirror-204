from lxml import etree as et


class OpiPoints(object):

    def render(self, widget_node, tag_name, points_model):
        points_node = et.SubElement(widget_node, tag_name)
        for (x, y) in points_model:
            point_node = et.SubElement(points_node, 'point')
            point_node.set('x', str(x))
            point_node.set('y', str(y))
