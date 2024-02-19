import os

from ament_index_python.resources import get_resource
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget
from python_qt_binding import loadUi
from rosidl_runtime_py.utilities import get_message
from rqt_py_common.topic_completer import TopicCompleter

from .utils import generate_field_evals, get_topic_type


class BarGaugeWidget(QWidget):

    updateValueSignal = pyqtSignal(int, int)

    def __init__(self, node):
        super().__init__()
        self.setObjectName('BarGauge_widget')

        self.node = node
        self.sub = None

        _, package_path = get_resource('packages', 'rqt_gauges')
        ui_file = os.path.join(package_path, 'share',
                               'rqt_gauges', 'resource', 'bar_gauge.ui')
        loadUi(ui_file, self)

        # Topic Completer
        self.topic_to_subscribe.setNode(self.node)
        self._topic_completer = TopicCompleter(self.topic_to_subscribe)
        self._topic_completer.update_topics(self.node)
        self.topic_to_subscribe.setCompleter(self._topic_completer)

        # Signals Connection
        self.subscribe.pressed.connect(self.updateSubscription)
        self.updateValueSignal.connect(self.updateValue)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            topic_name = str(event.mimeData().text())
        else:
            droped_item = event.source().selectedItems()[0]
            topic_name = str(droped_item.data(0, Qt.UserRole))

        self.topic_to_subscribe.setText(topic_name)
        self.updateSubscription()

        event.accept()

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
                self.callback,
                10)

    @pyqtSlot(int, int)
    def updateValue(self, value, raw_value):
        self.bar_gauge.setValue(value)
        self.value_label.setText(str(raw_value / 100.0))

    def callback(self, msg):
        value = msg
        for f in self.field_evals:
            value = f(value)
        if value is not None and (type(value) == int or type(value) == float
                                  or type(value) == str):
            raw_value = int(value*100)
            if value < 0:
                value = 0
                print('The value is not between 0 and 1')
            elif value > 1:
                value = 1
                print('The value is not between 0 and 1')

            self.updateValueSignal.emit(int(value*100), raw_value)
        else:
            print('The value is not valid')
