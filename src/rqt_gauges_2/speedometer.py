from qt_gui.plugin import Plugin
from .speedometer_widget import *

class Speedometer(Plugin):

    def __init__(self, context):
        super(Speedometer, self).__init__(context)
        self.setObjectName('Speedometer')

        self._context = context
        self._node = context.node

        self._widget = SpeedometerWidget(self._node)
        context.add_widget(self._widget)

    
