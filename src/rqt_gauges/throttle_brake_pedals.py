from qt_gui.plugin import Plugin

from .throttle_brake_pedals_widget import ThrottleBrakePedalsWidget


class ThrottleBrakePedals(Plugin):

    def __init__(self, context):
        super().__init__(context)
        self.setObjectName('ThrottleBrakePedals')

        self._context = context
        self._node = context.node

        self._widget = ThrottleBrakePedalsWidget(self._node)
        context.add_widget(self._widget)
