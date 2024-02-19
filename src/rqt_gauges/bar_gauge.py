from qt_gui.plugin import Plugin

from .bar_gauge_widget import BarGaugeWidget


class BarGauge(Plugin):

    def __init__(self, context):
        super().__init__(context)
        self.setObjectName('BarGauge')

        self._context = context
        self._node = context.node

        self._widget = BarGaugeWidget(self._node)
        context.add_widget(self._widget)
