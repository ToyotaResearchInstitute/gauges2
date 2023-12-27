import os

from ament_index_python.resources import get_resource
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget
from python_qt_binding import loadUi
from rosidl_runtime_py.utilities import get_message
from rqt_py_common.topic_completer import TopicCompleter

from .utils import generate_field_evals, get_topic_type


class SpeedometerWidget(QWidget):

    def __init__(self, node):
        super().__init__()
        self.setObjectName('Speedometer_widget')

        self.node = node
        self.sub = None

        _, package_path = get_resource('packages', 'rqt_gauges')
        ui_file = os.path.join(package_path, 'share', 'rqt_gauges', 'resource', 'speedometer.ui')
        loadUi(ui_file, self)

        self.topic_to_subscribe.setNode(self.node)

        self._topic_completer = TopicCompleter(self.topic_to_subscribe)
        self._topic_completer.update_topics(self.node)
        self.topic_to_subscribe.setCompleter(self._topic_completer)

        # Objects Properties
        self.max_value.setAlignment(Qt.AlignCenter)
        self.min_value.setAlignment(Qt.AlignCenter)

        self.max_value.setPlaceholderText(str(self.speedometer_gauge.maxValue))
        self.min_value.setPlaceholderText(str(self.speedometer_gauge.minValue))

        # Signals Connection
        self.min_value.textChanged.connect(self.updateMinValue)
        self.max_value.textChanged.connect(self.updateMaxValue)
        self.units.currentTextChanged.connect(self.updateUnits)
        self.subscribe_button.pressed.connect(self.updateSubscription)

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

    @pyqtSlot()
    def updateSubscription(self):
        if self.node.destroy_subscription(self.sub):
            print('Previous subscription deleted')
        else:
            print('There was no previous subscription')
        topic_path = self.topic_to_subscribe.text()
        topic_type, topic_name, fields = get_topic_type(self.node, topic_path)
        self.field_evals = generate_field_evals(fields)
        if topic_type is not None and self.field_evals is not None:
            print('Subscribing to:', topic_name, 'Type:', topic_type, 'Field:', fields)
            data_class = get_message(topic_type)
            self.sub = self.node.create_subscription(
                data_class,
                topic_name,
                self.speedometer_callback,
                10)

    def speedometer_callback(self, msg):
        value = msg
        for f in self.field_evals:
            value = f(value)
        if value is not None:
            if type(value) == int or type(value) == float or type(value) == str:
                self.speedometer_gauge.updateValue(float(value))
            else:
                self.speedometer_gauge.updateValue(self.speedometer_gauge.minValue)
        else:
            self.speedometer_gauge.updateValue(self.speedometer_gauge.minValue)
