import lxml.etree as et


class OpiText(object):

    def render(self, widget_node, tag_name, model):
        text_node = et.SubElement(widget_node, tag_name)
        if model is True:
            text_node.text = 'true'
        elif model is False:
            text_node.text = 'false'
        else:
            text_node.text = str(model)
