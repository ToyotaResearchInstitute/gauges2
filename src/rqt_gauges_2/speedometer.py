from qt_gui.plugin import Plugin
from .speedometer_widget import *

def is_number_type(type):
    number_types = [
        'int8', 'uint8',
        'int16', 'uint16',
        'int32', 'uint32',
        'int64', 'uint64',
        'float', 'float32', 'float64',
        'double', 'long double']
    return type in number_types

class Speedometer(Plugin):

    def __init__(self, context):
        super(Speedometer, self).__init__(context)
        self.setObjectName('Speedometer')

        self._context = context
        self._node = context.node

        self._widget = SpeedometerWidget(self._node)
        context.add_widget(self._widget)

    
