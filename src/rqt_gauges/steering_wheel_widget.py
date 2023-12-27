import os

from ament_index_python.resources import get_resource
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget
from python_qt_binding import loadUi
from rosidl_runtime_py.utilities import get_message
from rqt_py_common.topic_completer import TopicCompleter

from .utils import generate_field_evals, get_topic_type


class SteeringWheelWidget(QWidget):

    def __init__(self, node):
        super().__init__()
        self.setObjectName('SteeringWheel_widget')

        self.node = node
        self.sub = None

        _, package_path = get_resource('packages', 'rqt_gauges')
        ui_file = os.path.join(package_path, 'share', 'rqt_gauges',
                               'resource', 'steering_wheel.ui')
        loadUi(ui_file, self)

        self.topic_to_subscribe.setNode(self.node)

        self._topic_completer = TopicCompleter(self.topic_to_subscribe)
        self._topic_completer.update_topics(self.node)
        self.topic_to_subscribe.setCompleter(self._topic_completer)

        # Objects Properties
        self.max_value.setAlignment(Qt.AlignCenter)

        self.max_value.setPlaceholderText(str(self.steering_wheel_gauge.maxValue))

        self.max_value.textChanged.connect(self.updateMaxValue)
        self.subscribe_button.pressed.connect(self.updateSubscription)

    @pyqtSlot()
    def updateMaxValue(self):
        new_max_value = self.max_value.toPlainText()
        if new_max_value.isnumeric():
            self.steering_wheel_gauge.setMaxValue(int(new_max_value))
        else:
            self.steering_wheel_gauge.setMaxValue(45)

    @pyqtSlot()
    def updateSubscription(self):
        if self.node.destroy_subscription(self.sub):
            print('Previous subscription deleted')
        else:
            print('There was no previous subscription')
        topic_path = self.topic_to_subscribe.text()
        topic_type, topic_name, fields = get_topic_type(self.node, topic_path)
        self.field_evals = generate_field_evals(fields)
        if topic_type is not None:
            print('Subscribing to:', topic_name, 'Type:', topic_type, 'Field:', fields)
            data_class = get_message(topic_type)
            self.sub = self.node.create_subscription(
                data_class,
                topic_name,
                self.steering_wheel_callback,
                10)

    def steering_wheel_callback(self, msg):
        value = msg
        for f in self.field_evals:
            value = f(value)
        if value is not None:
            if type(value) == int or type(value) == float or type(value) == str:
                self.steering_wheel_gauge.updateValue(float(value))
            else:
                self.steering_wheel_gauge.updateValue(0)
        else:
            self.steering_wheel_gauge.updateValue(0)
