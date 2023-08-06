import collections
import re

import lxml.etree as et


class OpiWidget(object):

    def __init__(self, text_renderer):
        self._text_renderer = text_renderer
        self._renderers = collections.defaultdict(lambda: self._text_renderer)

    def add_renderer(self, tag, renderer):
        self._renderers[tag] = renderer

    def render(self, model, parent, res={}):
        if parent is None:
            node = et.Element(model.get_type_name())
        else:
            node = et.SubElement(parent, model.get_type_name())
        #
        res.update(model.get_resources())
        #
        node.set('typeId', model.get_type_id())
        node.set('version', model.get_version())
        for var, val in sorted(vars(model).items()):
            if all(re.match(rf'^{w}', var) == None for w in ('phoebus', '_')):
                self._renderers[var].render(node, var, val)
        for child in model.get_children():
            self.render(child, node, res)

        return node
