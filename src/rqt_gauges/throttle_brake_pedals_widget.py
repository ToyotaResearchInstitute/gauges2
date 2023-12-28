import os

from ament_index_python.resources import get_resource
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from python_qt_binding import loadUi
from rosidl_runtime_py.utilities import get_message
from rqt_py_common.topic_completer import TopicCompleter

from .utils import generate_field_evals, get_topic_type


class ThrottleBrakePedalsWidget(QWidget):

    def __init__(self, node):
        super().__init__()
        self.setObjectName('ThrottleBrakePedals_widget')

        self.node = node
        self.throttle_sub = None
        self.brake_sub = None

        _, package_path = get_resource('packages', 'rqt_gauges')
        ui_file = os.path.join(package_path, 'share',
                               'rqt_gauges', 'resource', 'throttle_brake_pedals.ui')
        loadUi(ui_file, self)

        # Throttle Topic Completer
        self.throttle_topic_to_subscribe.setNode(self.node)
        self._throttle_topic_completer = TopicCompleter(self.throttle_topic_to_subscribe)
        self._throttle_topic_completer.update_topics(self.node)
        self.throttle_topic_to_subscribe.setCompleter(self._throttle_topic_completer)

        # Brake Topic Completer
        self.brake_topic_to_subscribe.setNode(self.node)
        self._brake_topic_completer = TopicCompleter(self.brake_topic_to_subscribe)
        self._brake_topic_completer.update_topics(self.node)
        self.brake_topic_to_subscribe.setCompleter(self._brake_topic_completer)

        # Signals Connection
        self.throttle_subscribe.pressed.connect(self.throttleUpdateSubscription)
        self.brake_subscribe.pressed.connect(self.brakeUpdateSubscription)

    @pyqtSlot()
    def throttleUpdateSubscription(self):
        if self.node.destroy_subscription(self.throttle_sub):
            print('Previous subscription deleted')
        else:
            print('There was no previous subscription')
        topic_path = self.throttle_topic_to_subscribe.text()
        topic_type, topic_name, fields = get_topic_type(self.node, topic_path)
        self.throttle_field_evals = generate_field_evals(fields)
        if topic_type is not None:
            print('Subscribing to:', topic_name, 'Type:', topic_type, 'Field:', fields)
            data_class = get_message(topic_type)
            self.throttle_sub = self.node.create_subscription(
                data_class,
                topic_name,
                self.throttle_callback,
                10)

    @pyqtSlot()
    def brakeUpdateSubscription(self):
        if self.node.destroy_subscription(self.brake_sub):
            print('Previous subscription deleted')
        else:
            print('There was no previous subscription')
        topic_path = self.brake_topic_to_subscribe.text()
        topic_type, topic_name, fields = get_topic_type(self.node, topic_path)
        self.brake_field_evals = generate_field_evals(fields)
        if topic_type is not None:
            print('Subscribing to:', topic_name, 'Type:', topic_type, 'Field:', fields)
            data_class = get_message(topic_type)
            self.brake_sub = self.node.create_subscription(
                data_class,
                topic_name,
                self.brake_callback,
                10)

    def throttle_callback(self, msg):
        value = msg
        for f in self.throttle_field_evals:
            value = f(value)
        if value is not None and (type(value) == int or type(value) == float
                                  or type(value) == str):
            if value <= 1 and value >= 0:
                self.throttle_pedal.setValue(int(value*100))
                self.throttle_label.setText(str(value))
            else:
                print('The throttle pedal value is not between 0 and 1')
        else:
            print('The throttle pedal value is not valid')

    def brake_callback(self, msg):
        value = msg
        for f in self.brake_field_evals:
            value = f(value)
        if value is not None and (type(value) == int or type(value) == float
                                  or type(value) == str):
            if value <= 1 and value >= 0:
                self.brake_pedal.setValue(int(value*100))
                self.brake_label.setText(str(value))
            else:
                print('The brake pedal value is not between 0 and 1')
        else:
            print('The brake pedal value is not valid')
