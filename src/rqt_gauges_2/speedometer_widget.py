import math
import os

from ament_index_python.resources import get_resource
from python_qt_binding import loadUi
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSlot

class SpeedometerWidget(QWidget):
    def __init__(self, node, initial_topics=None):
        super(SpeedometerWidget, self).__init__()
        self.setObjectName('Speedometer_widget')

        self._node = node
        self._initial_topics = initial_topics

        _, package_path = get_resource('packages', 'rqt_gauges_2')
        ui_file = os.path.join(package_path, 'share', 'rqt_gauges_2', 'resource', 'speedometer.ui')
        loadUi(ui_file, self)

        # Objects Properties
        self.max_value.setAlignment(Qt.AlignCenter)
        self.min_value.setAlignment(Qt.AlignCenter)

        self.max_value.setPlaceholderText(str(self.speedometer_gauge.maxValue))
        self.min_value.setPlaceholderText(str(self.speedometer_gauge.minValue))
        self.topic_to_subscribe.setPlaceholderText("/test_topic")

        # Signals Connection
        self.min_value.textChanged.connect(self.updateMinValue)
        self.max_value.textChanged.connect(self.updateMaxValue)
        self.units.currentTextChanged.connect(self.updateUnits)

    @pyqtSlot()
    def updateMinValue(self):
        new_min_value = self.min_value.toPlainText()
        if new_min_value.isnumeric():
            self.speedometer_gauge.setMinValue(int(new_min_value))
        else:
            self.speedometer_gauge.setMinValue(0)

    @pyqtSlot()
    def updateMaxValue(self):
        new_max_value = self.max_value.toPlainText()
        if new_max_value.isnumeric():
            self.speedometer_gauge.setMaxValue(int(new_max_value))
        else:
            self.speedometer_gauge.setMaxValue(180)

    @pyqtSlot(str)
    def updateUnits(self, new_units):
        self.speedometer_gauge.units = new_units
        self.speedometer_gauge.update()

