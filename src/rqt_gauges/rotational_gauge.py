import math

from PyQt5.QtCore import pyqtSignal, QRect, Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QFontMetrics, QPainter, QPen
from PyQt5.QtWidgets import QWidget


class RotationalGauge(QWidget):
    # This class creates a rotational gauge.

    updateValueSignal = pyqtSignal(float)

    def __init__(self, parent=None):
        # Constructor method of the class, initializes all the variables needed to create
        # # the gauge.

        super().__init__(parent)

        self.raw_value = 0
        self.value = 0
        self.width = 400
        self.height = 400
        self.progress_width = 25
        self.progress_rounded_cap = True
        self.progress_color = 0x39F030
        self.circle_max_angle = 135
        self.font_size = 40
        self.scale_font_size = 15
        self.font_family = 'Verdana'
        self.suffix = '°'
        self.text_color = 0x000000
        self.enable_shadow = True

        self.angle_offset = 0
        self.minValue = -45
        self.maxValue = 45

        self.widget_diameter = min(self.width, self.height)
        self.resize(self.width, self.height)

        self.scale_line_outer_start = int(self.widget_diameter / 2)
        self.scale_line_length = int((self.widget_diameter / 2) - (self.widget_diameter / 20))

        self.text_radius_factor = 0.75
        self.text_radius = self.widget_diameter/2 * self.text_radius_factor

    def draw_big_scaled_marker(self, start_angle_value: int, angle_size: int, scala_count: int):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width / 2, self.height / 2)

        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        painter.rotate(start_angle_value - self.angle_offset)
        steps_size = (float(angle_size) / float(scala_count))

        for _ in range(scala_count+1):
            painter.drawLine(int(self.scale_line_length), 0, int(self.scale_line_outer_start), 0)
            painter.rotate(steps_size)
        painter.end()

    def create_scale_marker_values_text(self, scale_angle_start_value: int,
                                        scale_angle_size: int, scalaCount: int):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.translate(self.width / 2, self.height / 2)
        font = QFont(self.font_family, self.scale_font_size, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()
        pen_shadow.setBrush(QColor(0, 0, 0, 255))
        painter.setPen(pen_shadow)

        scale_per_div = int((self.maxValue - self.minValue) / scalaCount)

        angle_distance = (float(scale_angle_size) / float(scalaCount))
        for i in range(scalaCount + 1):
            text = str(int(self.minValue + scale_per_div * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.font_family, self.scale_font_size))
            angle = angle_distance * i + float(scale_angle_start_value - self.angle_offset)
            x = int(self.text_radius * math.cos(math.radians(angle)))
            y = int(self.text_radius * math.sin(math.radians(angle)))

            text = [x - int(w/2), y - int(h/2), int(w), int(h), Qt.AlignCenter, text]
            painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])
        painter.end()

    def updateValue(self, value: float):
        # Updates the value that the gauge is indicating.
        # Args:
        #   value: Value to update the gauge with.
        self.raw_value = value
        value = max(value, self.minValue)
        value = min(value, self.maxValue)
        self.value = value
        self.repaint()

    def setMaxValue(self, max_value):
        # Modifies the maximum value of the gauge
        # Args:
        #   max: Value to update the maximum value of the gauge.
        if self.value > max_value:
            self.value = max_value
        if max_value <= self.minValue:
            self.maxValue = self.minValue + 1
            self.minValue = -self.maxValue + 1
        else:
            self.maxValue = max_value
            self.minValue = -max_value

        self.update()

    def draw_background_circle(self):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.lightGray, Qt.SolidPattern))
        painter.drawEllipse(0, 0, 400, 400)
        painter.end()

    def paintEvent(self, event):
        # Size variables
        width = self.width - self.progress_width
        height = self.height - self.progress_width
        margin = int(self.progress_width / 2)
        value = int(self.value * self.circle_max_angle / self.maxValue)

        # Draw Circle
        self.draw_background_circle()

        # Painter
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(QFont(self.font_family, self.font_size))

        # Rectangle
        rect = QRect(0, 0, self.width, self.height)
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

        # Pen to draw progress bar
        pen = QPen()
        pen.setColor(QColor(self.progress_color))
        pen.setWidth(self.progress_width)
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)

        # Create Arc
        painter.setPen(pen)
        painter.drawArc(margin, margin, width, height, 90 * 16, -value * 16)

        # Create Gauge Text
        pen.setColor(QColor(self.text_color))
        painter.setPen(pen)
        painter.drawText(rect, Qt.AlignCenter, f'{self.raw_value:.2f}{self.suffix}')
        # End Painter
        painter.end()

        self.draw_big_scaled_marker(131, 278, 5)
        self.create_scale_marker_values_text(131, 278, 5)
