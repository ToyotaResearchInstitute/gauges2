import os

from ament_index_python.resources import get_resource
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from python_qt_binding import loadUi
from rosidl_runtime_py.utilities import get_message
from rqt_py_common.topic_completer import TopicCompleter


def get_topic_type(node, topic):
    """
    Subroutine for getting the topic type.

    (nearly identical to rostopic._get_topic_type, except it returns rest of name instead of fn)

    :returns: topic type, real topic name, and rest of name referenced
      if the topic points to a field within a topic, e.g. /rosout/msg, ``str, str, str``
    """
    val = node.get_topic_names_and_types()
    matches = [(t, t_types) for t, t_types in val if t == topic or topic.startswith(t + '/')]
    for t, t_types in matches:
        for t_type in t_types:
            if t_type == topic:
                return t_type, None, None
        for t_type in t_types:
            if t_type != '*':
                return t_type, t, topic[len(t):]
    return None, None, None


def _array_eval(field_name, slot_num):
    """
    Array Evaluation.

    :param field_name: name of field to index into, ``str``
    :param slot_num: index of slot to return, ``str``
    :returns: fn(msg_field)->msg_field[slot_num]
    """
    def fn(f):
        return getattr(f, field_name).__getitem__(slot_num)
    return fn


def _field_eval(field_name):
    """
    Field evaluation.

    :param field_name: name of field to return, ``str``
    :returns: fn(msg_field)->msg_field.field_name
    """
    def fn(f):
        return getattr(f, field_name)
    return fn


def generate_field_evals(fields):
    evals = []
    fields = [f for f in fields.split('/') if f]
    for f in fields:
        if '[' in f:
            field_name, rest = f.split('[')
            slot_num = int(rest[:rest.find(']')])
            evals.append(_array_eval(field_name, slot_num))
        else:
            evals.append(_field_eval(f))
    return evals


class SteeringWheelWidget(QWidget):

    def __init__(self, node):
        super().__init__()
        self.setObjectName('SteeringWheel_widget')

        self.node = node
        self.sub = None

        _, package_path = get_resource('packages', 'rqt_gauges_2')
        ui_file = os.path.join(package_path, 'share', 'rqt_gauges_2',
                               'resource', 'steering_wheel.ui')
        loadUi(ui_file, self)

        self.topic_to_subscribe.setNode(self.node)

        self._topic_completer = TopicCompleter(self.topic_to_subscribe)
        self._topic_completer.update_topics(self.node)
        self.topic_to_subscribe.setCompleter(self._topic_completer)

        self.subscribe_button.pressed.connect(self.updateSubscription)

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
        self.steering_wheel_gauge.updateValue(float(value))
