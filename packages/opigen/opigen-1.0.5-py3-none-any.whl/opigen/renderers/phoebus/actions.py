import re
import lxml.etree as et
from opigen.opimodel import actions
from . import text

EXIT_SCRIPT = (
    'importClass(org.csstudio.display.builder.runtime.script.ScriptUtil);'
    'ScriptUtil.closeDisplay(widget);')


class OpiAction(object):
    """Base class for action renderers."""

    def __init__(self, text_renderer):
        self.text = text_renderer
        self._action_type = self.ACTION_TYPE

    def render(self, actions_node, action_model):
        action_node = et.SubElement(actions_node, 'action')
        action_node.set('type', self.ACTION_TYPE)
        for key, value in vars(action_model).items():
            r = re.match(r'^phoebus_(.*)', key)
            if r is None:
                continue
            _attr_name = r.group(1)
            self.text.render(action_node, _attr_name, value)
        return action_node


class OpiWritePv(OpiAction):
    """Renderer for write PV actions."""
    ACTION_TYPE = 'write_pv'


class OpiExecuteCommand(OpiAction):
    """Renderer for execute command actions."""
    ACTION_TYPE = 'command'


class OpiOpen(OpiAction):
    """Renderer for open OPI actions."""
    ACTION_TYPE = 'open_display'
    MACRO_ERROR = 'Invalid macro {}:{} (error {})'

    def render(self, actions_node, action_model):
        action_node = super(OpiOpen, self).render(actions_node, action_model)
        macros_node = et.SubElement(action_node, 'macros')
        # phoebus does not have this option
        #parent_macros_node = et.SubElement(macros_node, 'include_parent_macros')
        #parent_macros_node.text = 'true' if action_model.get_parent_macros() else 'false'
        for key, value in action_model.get_macros().items():
            try:
                key_node = et.SubElement(macros_node, key)
                key_node.text = str(value)
            except (TypeError, ValueError) as e:
                raise ValueError(self.MACRO_ERROR.format(key, value, e))
        return action_node


class OpiExit(OpiAction):
    """Render for exit OPI actions."""
    ACTION_TYPE = 'execute'

    def render(self, actions_node, action_model):
        """Render an exit action.

        Args:
            actions_node to be parent of the action
            action_model representing the exit action
        """
        # In CSS exit happens to use javascript.  Add properties to help with
        # rendering.
        action_model._action_type = 'execute'
        action_model.embedded = True
        # Render the javascript
        action_node = super(OpiExit, self).render(actions_node, action_model)
        script_node = et.SubElement(action_node, 'script')
        script_node.set('file', 'EmbeddedJs')
        code_node = et.SubElement(script_node, 'text')
        code_node.text = et.CDATA(EXIT_SCRIPT)
        desc_node = et.SubElement(action_node, 'description')
        desc_node.text = 'Exit'


class OpiActions(object):
    """Renderer for actions."""

    ACTION_MAPPING = {
        actions.ExecuteCommand: OpiExecuteCommand,
        actions.WritePv: OpiWritePv,
        actions.Exit: OpiExit,
        actions.OpenOpi: OpiOpen
    }

    def render(self, widget_node, tag_name, actions_model):
        if actions_model:
            actions_node = et.SubElement(widget_node, tag_name)
            # phoebus does not have 'hook' or 'hook_all' option
            #hook_first = 'true' if actions_model.get_hook_first() else 'false'
            #hook_all = 'true' if actions_model.get_hook_all() else 'false'
            #actions_node.set('hook', hook_first)
            #actions_node.set('hook_all', hook_all)
            for action_model in actions_model:
                action_class = OpiActions.ACTION_MAPPING[type(action_model)]
                renderer = action_class(text.OpiText())
                renderer.render(actions_node, action_model)
