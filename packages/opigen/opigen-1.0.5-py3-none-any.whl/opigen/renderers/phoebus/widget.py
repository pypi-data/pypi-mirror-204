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
        _type = model.get_type()
        if _type is not None:
            node.set('type', _type)
        node.set('version', model.get_version_phoebus())
        for var, val in sorted(vars(model).items()):
            # only select the attribute name starts with 'phoebus'
            r = re.match(r'^phoebus_(.*)', var)
            if r is None:
                continue
            _attr_name = r.group(1)
            self._renderers[_attr_name].render(node, _attr_name, val)
        for child in model.get_children():
            self.render(child, node, res)

        return node
