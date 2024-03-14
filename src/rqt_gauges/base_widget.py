from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget
from python_qt_binding import loadUi
from rosidl_runtime_py.utilities import get_message
from rqt_py_common.topic_completer import TopicCompleter

from .utils import generate_field_evals, get_topic_type


class BaseWidget(QWidget):

    def __init__(self, node, name, ui_path):
        super().__init__()
        self.setObjectName(name)

        self.node = node
        self.sub = None

        loadUi(ui_path, self)

        self.topic_to_subscribe.setNode(self.node)

        self._topic_completer = TopicCompleter(self.topic_to_subscribe)
        self._topic_completer.update_topics(self.node)
        self.topic_to_subscribe.setCompleter(self._topic_completer)

        try:
            getattr(self.gauge, 'maxValue')
            self.max_value.setAlignment(Qt.AlignCenter)
            self.max_value.setPlaceholderText(str(self.gauge.maxValue))
            self.max_value.textChanged.connect(self.updateMaxValue)
        except AttributeError:
            pass

        try:
            getattr(self.gauge, 'minValue')
            self.min_value.setAlignment(Qt.AlignCenter)
            self.min_value.setPlaceholderText(str(self.gauge.minValue))
            self.min_value.textChanged.connect(self.updateMinValue)
        except AttributeError:
            pass

        try:
            getattr(self.gauge, 'units')
            self.units.textChanged.connect(self.updateUnits)
        except AttributeError:
            pass

        # Signals Connection
        self.subscribe_button.pressed.connect(self.updateSubscription)
        self.gauge.updateValueSignal.connect(self.updateValue)

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
    def updateMinValue(self):
        try:
            new_min_value = int(self.min_value.toPlainText())
            self.gauge.setMinValue(new_min_value)
        except ValueError:
            pass

    @pyqtSlot()
    def updateMaxValue(self):
        try:
            new_max_value = int(self.max_value.toPlainText())
            self.gauge.setMaxValue(new_max_value)
        except ValueError:
            pass

    @pyqtSlot(float)
    def updateValue(self, value):
        self.gauge.updateValue(value)

    @pyqtSlot()
    def updateUnits(self):
        self.gauge.units = self.units.toPlainText()
        self.gauge.update()

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
                self.callback,
                10)

    def callback(self, msg):
        value = msg
        for f in self.field_evals:
            value = f(value)
        if value is not None:
            if type(value) == int or type(value) == float or type(value) == str:
                self.gauge.updateValueSignal.emit(float(value))
            else:
                self.gauge.updateValueSignal.emit(self.gauge.minValue)
        else:
            self.gauge.updateValueSignal.emit(self.gauge.minValue)
