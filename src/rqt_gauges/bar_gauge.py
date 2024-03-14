from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QProgressBar, QWidget


class BarGauge(QWidget):

    updateValueSignal = pyqtSignal(float)

    def __init__(self, parent):
        # Constructor method of the class, initializes all the variables needed to create
        # the gauge.

        super().__init__(parent)

        self.minValue = 0.0
        self.maxValue = 100.0
        self.raw_value = self.minValue
        self.value = self.minValue

        # Progress bar
        self.bar = QProgressBar(parent)
        self.bar.setGeometry(150, 126, 51, 301)
        self.bar.setOrientation(Qt.Vertical)
        self.bar.setRange(int(self.minValue), int(self.maxValue))

        # Value label
        self.valueLabel = QLabel(parent)
        self.valueLabel.setGeometry(65, 425, 221, 61)
        self.valueLabel.setAlignment(Qt.AlignCenter)
        self.valueLabel.setStyleSheet('QLabel{font-size: 25pt;}')
        self.valueLabel.setText('0.0')

    def updateValue(self, value: float):
        # Updates the value that the gauge is indicating.
        # Args:
        #   value: Value to update the gauge with.
        self.raw_value = value
        value = max(value, self.minValue)
        value = min(value, self.maxValue)
        self.value = value
        self.bar.setValue(int(self.value))
        self.valueLabel.setText(str(self.raw_value))

        self.update()

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

        self.bar.setRange(int(self.minValue), int(self.maxValue))
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

        self.bar.setRange(int(self.minValue), int(self.maxValue))
        self.update()
