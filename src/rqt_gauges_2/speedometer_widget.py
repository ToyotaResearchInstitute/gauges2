import math
import os

from ament_index_python.resources import get_resource
from python_qt_binding import loadUi
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

class SpeedometerWidget(QWidget):
    def __init__(self, node, initial_topics=None):
        super(SpeedometerWidget, self).__init__()
        self.setObjectName('Speedometer_widget')

        self._node = node
        self._initial_topics = initial_topics

        _, package_path = get_resource('packages', 'rqt_gauges_2')
        ui_file = os.path.join(package_path, 'share', 'rqt_gauges_2', 'resource', 'speedometer.ui')
        loadUi(ui_file, self)

        self.max_value.setAlignment(Qt.AlignCenter)
        self.min_value.setAlignment(Qt.AlignCenter)
        self.units.setAlignment(Qt.AlignCenter)

        self.max_value.setPlaceholderText(str(self.speedometer_gauge.maxValue))
        self.min_value.setPlaceholderText(str(self.speedometer_gauge.minValue))
        self.units.setPlaceholderText(self.speedometer_gauge.units)
        self.topic_to_subscribe.setPlaceholderText("/test_topic")

