from qt_gui.plugin import Plugin
from PyQt5 import QtCore, QtGui, QtWidgets
from .speedometer_widget import *
from std_msgs.msg import Int16

class Gauges2(Plugin):

    def __init__(self, context):
        super(Gauges2, self).__init__(context)
        self.setObjectName('Gauges2')

        self._context = context
        self._node = context.node
        self.speedometer_subscriber = self._node.create_subscription(
            Int16,
            '/test_topic',
            self.speedometer_callback,
            10)
        self._widget = SpeedometerWidget()
        context.add_widget(self._widget)

    def speedometer_callback(self, msg):
        self._widget.updateValue(msg.data)
