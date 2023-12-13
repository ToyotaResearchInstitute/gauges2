import os

from ament_index_python.resources import get_resource
from PyQt5.QtCore import pyqtSlot, Qt
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
    Array evaluation.

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


class SpeedometerWidget(QWidget):

    def __init__(self, node):
        super().__init__()
        self.setObjectName('Speedometer_widget')

        self.node = node
        self.sub = None

        _, package_path = get_resource('packages', 'rqt_gauges_2')
        ui_file = os.path.join(package_path, 'share', 'rqt_gauges_2', 'resource', 'speedometer.ui')
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
        if topic_type is not None:
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
        self.speedometer_gauge.updateValue(float(value))
