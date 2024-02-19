from qt_gui.plugin import Plugin

from .rotational_widget import RotationalWidget


class Rotational(Plugin):

    def __init__(self, context):
        super().__init__(context)
        self.setObjectName('Rotational')

        self._context = context
        self._node = context.node

        self._widget = RotationalWidget(self._node)
        context.add_widget(self._widget)
