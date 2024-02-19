from qt_gui.plugin import Plugin

from .dial_widget import DialWidget


class Dial(Plugin):

    def __init__(self, context):
        super().__init__(context)
        self.setObjectName('Dial')

        self._context = context
        self._node = context.node

        self._widget = DialWidget(self._node)
        context.add_widget(self._widget)
