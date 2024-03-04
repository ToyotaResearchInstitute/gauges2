import math

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QProgressBar, QWidget


class BarGauge(QWidget):

    updateValueSignal = pyqtSignal(float)

    def __init__(self, node):
        # Constructor method of the class, initializes all the variables needed to create
        # the gauge.

        super().__init__()

        self.minValue = 0
        self.maxValue = 1
        self.raw_value = self.minValue
        self.value = self.minValue

    def updateValue(self, value: float):
        # Updates the value that the gauge is indicating.
        # Args:
        #   value: Value to update the gauge with.
        self.raw_value = value
        value = max(value, self.minValue)
        value = min(value, self.maxValue)
        self.value = value
        self.repaint()

    def setMinValue(self, min_value):
        # Modifies the minimum value of the gauge
        # Args:
        #   min: Value to update the minimum value of the gauge.
        if self.value < min_value:
            self.value = min_value
        if min_value >= self.maxValue:
            self.minValue = self.maxValue - 1
        else:
            self.minValue = min_value

        self.update()

    def setMaxValue(self, max_value):
        # Modifies the maximum value of the gauge
        # Args:
        #   max: Value to update the maximum value of the gauge.
        if self.value > max_value:
            self.value = max_value
        if max_value <= self.minValue:
            self.maxValue = self.minValue + 1
        else:
            self.maxValue = max_value

        self.update()

    def paintEvent(self, event):
        self.bar_gauge.setValue(self.value)
        self.value_label.setText(str(raw_value / 100.0))
