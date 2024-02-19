import os

from ament_index_python.resources import get_resource
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget
from python_qt_binding import loadUi
from rosidl_runtime_py.utilities import get_message
from rqt_py_common.topic_completer import TopicCompleter

from .utils import generate_field_evals, get_topic_type


class RotationalWidget(QWidget):

    def __init__(self, node):
        super().__init__()
        self.setObjectName('Rotational_widget')

        self.node = node
        self.sub = None

        _, package_path = get_resource('packages', 'rqt_gauges')
        ui_file = os.path.join(package_path, 'share', 'rqt_gauges',
                               'resource', 'rotational.ui')
        loadUi(ui_file, self)

        self.topic_to_subscribe.setNode(self.node)

        self._topic_completer = TopicCompleter(self.topic_to_subscribe)
        self._topic_completer.update_topics(self.node)
        self.topic_to_subscribe.setCompleter(self._topic_completer)

        # Objects Properties
        self.max_value.setAlignment(Qt.AlignCenter)

        self.max_value.setPlaceholderText(str(self.rotational_gauge.maxValue))

        self.max_value.textChanged.connect(self.updateMaxValue)
        self.subscribe_button.pressed.connect(self.updateSubscription)
        self.rotational_gauge.updateValueSignal.connect(self.updateValue)

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
    def updateMaxValue(self):
        new_max_value = self.max_value.toPlainText()
        if new_max_value.isnumeric():
            self.rotational_gauge.setMaxValue(int(new_max_value))
        else:
            self.rotational_gauge.setMaxValue(45)

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
                self.rotational_callback,
                10)

    @pyqtSlot(float)
    def updateValue(self, value):
        self.rotational_gauge.updateValue(value)

    def rotational_callback(self, msg):
        value = msg
        for f in self.field_evals:
            value = f(value)
        if value is not None:
            if type(value) == int or type(value) == float or type(value) == str:
                self.rotational_gauge.updateValueSignal.emit(float(value))
            else:
                self.rotational_gauge.updateValueSignal.emit(0.0)
        else:
            self.rotational_gauge.updateValueSignal.emit(0.0)
