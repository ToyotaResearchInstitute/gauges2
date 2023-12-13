from qt_gui.plugin import Plugin

from .steering_wheel_widget import SteeringWheelWidget


class SteeringWheel(Plugin):

    def __init__(self, context):
        super().__init__(context)
        self.setObjectName('Speedometer')

        self._context = context
        self._node = context.node

        self._widget = SteeringWheelWidget(self._node)
        context.add_widget(self._widget)
