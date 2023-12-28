import math

from PyQt5.QtCore import QObject, QPoint, QPointF, Qt
from PyQt5.QtGui import (QColor, QConicalGradient, QFont, QFontMetrics, QPainter, QPen,
                         QPolygon, QPolygonF, QRadialGradient)
from PyQt5.QtWidgets import QWidget


class SpeedometerGauge(QWidget):
    # This class creates a gauge object that contains several elements such as a needle,
    # big and small scales and different circles painted with different colors to look like
    # a car Speedometer. It has the ability to modify the minimum and maximum values of the
    # gauge and the units the numbers are displaying. The class contains methods used to modify
    # the values explained before, the marked number of the gauge and the whole design as well.

    def __init__(self, parent=None):
        # Constructor method of the class, initializes all the variables needed to create
        # the gauge.

        super().__init__(parent)

        # Needle Attributes
        self.NeedleColor = QColor(0, 0, 0, 255)
        self.NeedleColorReleased = self.NeedleColor
        self.NeedleColorDrag = QColor(255, 0, 0, 255)
        self.value_needle = QObject

        # Scale Attributes
        self.ScaleValueColor = QColor(0, 0, 0, 255)
        self.DisplayValueColor = QColor(0, 0, 0, 255)
        self.CenterPointColor = QColor(0, 0, 0, 255)

        self.minValue = 0
        self.maxValue = 180
        self.value = self.minValue
        self.value_offset = 0
        self.valueNeedleSnapzone = 0.05
        self.last_value = 0

        self.center_horizontal_value = 0
        self.center_vertical_value = 0

        self.scale_angle_start_value = 135
        self.scale_angle_size = 270
        self.angle_offset = 0

        self.scalaCount = 9
        self.scala_subdiv_count = 5

        self.pen = QPen(QColor(0, 0, 0))

        self.bigScaleMarker = Qt.black
        self.fineScaleColor = Qt.black

        # Scale Text Attributes
        self.enable_scale_text = True
        self.scale_fontname = 'Verdana'
        self.initial_scale_fontsize = 14
        self.scale_fontsize = self.initial_scale_fontsize

        # Speed Text Attributes
        self.enable_value_text = True
        self.value_fontname = 'Verdana'
        self.initial_value_fontsize = 40
        self.value_fontsize = self.initial_value_fontsize
        self.text_radius_factor = 0.5

        self.units = ''

        # Gauge Attributes flags
        self.enableBarGraph = True
        self.enable_filled_Polygon = True
        self.enable_CenterPoint = True
        self.enable_fine_scaled_marker = True
        self.enable_big_scaled_marker = True
        self.enable_Needle_Polygon = True

        self.needle_scale_factor = 0.8

        self.gauge_color_outer_radius_factor = 1
        self.gauge_color_inner_radius_factor = 0.9

        self.update()
        self.setGaugeTheme()
        self.rescale_method()

    def setGaugeTheme(self):
        # This method defines the theme of the gauge, it is used to stablish the colors for each
        # section of the gauge.

        self.scale_polygon_colors = [[.00, Qt.red],
                                     [.18, Qt.yellow],
                                     [.35, Qt.green],
                                     [1, Qt.transparent]]

        self.needle_center_bg = [
                                [0, QColor(35, 40, 3, 255)],
                                [0.16, QColor(30, 36, 45, 255)],
                                [0.225, QColor(36, 42, 54, 255)],
                                [0.423963, QColor(19, 23, 29, 255)],
                                [0.580645, QColor(45, 53, 68, 255)],
                                [0.792627, QColor(59, 70, 88, 255)],
                                [0.935, QColor(30, 35, 45, 255)],
                                [1, QColor(30, 40, 3, 255)]
                                ]

        self.outer_circle_bg = [
                                [0, QColor(255, 255, 255, 255)],
                                [1, QColor(0, 0, 0, 255)]]

    def rescale_method(self):
        # This method adjust the gauge to the window size.
        if self.width() <= self.height():
            self.widget_diameter = self.width()
        else:
            self.widget_diameter = self.height()

        self.change_value_needle_style([QPolygon([
            QPoint(4, 30),
            QPoint(-4, 30),
            QPoint(-2, int(- self.widget_diameter / 2 * self.needle_scale_factor)),
            QPoint(0, int(- self.widget_diameter / 2 * self.needle_scale_factor - 6)),
            QPoint(2, int(- self.widget_diameter / 2 * self.needle_scale_factor))
        ])])

        self.scale_fontsize = int(self.initial_scale_fontsize * self.widget_diameter / 400)
        self.value_fontsize = int(self.initial_value_fontsize * self.widget_diameter / 400)

    def change_value_needle_style(self, design):
        self.value_needle = []
        for i in design:
            self.value_needle.append(i)
        self.update()

    def updateValue(self, value):
        # Updates the value that the gauge is indicating.
        # Args:
        #   value: Value to update the gauge with.

        if value <= self.minValue:
            self.value = self.minValue
        elif value >= self.maxValue:
            self.value = self.maxValue
        else:
            self.value = value
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

    def create_polygon_pie(self, outer_radius, inner_radius, start, length, bar_graph=True):
        # Creates the outer and inner circle of the gauge. Uses the

        polygon_pie = QPolygonF()
        n = 360     # angle steps size for full circle
        w = 360 / n   # angle per step
        x = 0
        y = 0

        if not self.enableBarGraph and bar_graph:
            length = int(round((length / (self.maxValue - self.minValue)) *
                         (self.value - self.minValue)))
            pass

        # Outer Circle
        for i in range(length+1):
            t = w * i + start - self.angle_offset
            x = outer_radius * math.cos(math.radians(t))
            y = outer_radius * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))

        # Inner Circle
        for i in range(length+1):
            t = w * (length - i) + start - self.angle_offset
            x = inner_radius * math.cos(math.radians(t))
            y = inner_radius * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))

        polygon_pie.append(QPointF(x, y))
        return polygon_pie

    def draw_filled_polygon(self, outline_pen_with=0):
        painter_filled_polygon = QPainter(self)
        painter_filled_polygon.setRenderHint(QPainter.Antialiasing)
        painter_filled_polygon.translate(self.width() / 2, self.height() / 2)
        painter_filled_polygon.setPen(Qt.NoPen)

        self.pen.setWidth(outline_pen_with)
        if outline_pen_with > 0:
            painter_filled_polygon.setPen(self.pen)

        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 2) - (self.pen.width() / 2)) *
            self.gauge_color_outer_radius_factor,
            (((self.widget_diameter / 2) - (self.pen.width() / 2)) *
             self.gauge_color_inner_radius_factor),
            self.scale_angle_start_value, self.scale_angle_size)

        grad = QConicalGradient(QPointF(0, 0), - self.scale_angle_size -
                                self.scale_angle_start_value + self.angle_offset - 1)

        for eachcolor in self.scale_polygon_colors:
            grad.setColorAt(eachcolor[0], eachcolor[1])
        painter_filled_polygon.setBrush(grad)

        painter_filled_polygon.drawPolygon(colored_scale_polygon)

    def draw_big_scaled_marker(self):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        my_painter.translate(self.width() / 2, self.height() / 2)

        self.pen = QPen(self.bigScaleMarker)
        self.pen.setWidth(2)
        my_painter.setPen(self.pen)

        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) / float(self.scalaCount))
        scale_line_outer_start = self.widget_diameter/2
        scale_line_lenght = (self.widget_diameter / 2) - (self.widget_diameter / 20)

        for i in range(self.scalaCount+1):
            my_painter.drawLine(int(scale_line_lenght), 0, int(scale_line_outer_start), 0)
            my_painter.rotate(steps_size)

    def create_scale_marker_values_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.scale_fontname, self.scale_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.ScaleValueColor)
        painter.setPen(pen_shadow)

        text_radius_factor = 0.8
        text_radius = self.widget_diameter/2 * text_radius_factor

        scale_per_div = int((self.maxValue - self.minValue) / self.scalaCount)

        angle_distance = (float(self.scale_angle_size) / float(self.scalaCount))
        for i in range(self.scalaCount + 1):
            text = str(int(self.minValue + scale_per_div * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.scale_fontname, self.scale_fontsize, QFont.Bold))
            angle = angle_distance * i + float(self.scale_angle_start_value - self.angle_offset)
            x = int(text_radius * math.cos(math.radians(angle)))
            y = int(text_radius * math.sin(math.radians(angle)))

            text = [x - int(w/2), y - int(h/2), int(w), int(h), Qt.AlignCenter, text]
            painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])

    def create_fine_scaled_marker(self):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        my_painter.translate(self.width() / 2, self.height() / 2)

        my_painter.setPen(self.fineScaleColor)
        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) / float(self.scalaCount
                      * self.scala_subdiv_count))
        scale_line_outer_start = self.widget_diameter/2
        scale_line_lenght = (self.widget_diameter / 2) - (self.widget_diameter / 40)
        for i in range((self.scalaCount * self.scala_subdiv_count)+1):
            my_painter.drawLine(int(scale_line_lenght), 0, int(scale_line_outer_start), 0)
            my_painter.rotate(steps_size)

    def create_value_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, self.value_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor
        text = str(int(self.value))
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname, self.value_fontsize, QFont.Bold))

        angle_end = float(self.scale_angle_start_value + self.scale_angle_size - 360)
        angle = (angle_end - self.scale_angle_start_value) / 2 + self.scale_angle_start_value

        x = int(text_radius * math.cos(math.radians(angle)))
        y = int(text_radius * math.sin(math.radians(angle)))
        text = [x - int(w/2), y - int(h/2), int(w), int(h), Qt.AlignCenter, text]
        painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])

    def create_units_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, int(self.value_fontsize / 2.5), QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        text = str(self.units)
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname, int(self.value_fontsize / 2.5), QFont.Bold))

        angle_end = float(self.scale_angle_start_value + self.scale_angle_size + 180)
        angle = (angle_end - self.scale_angle_start_value) / 2 + self.scale_angle_start_value

        x = int(text_radius * math.cos(math.radians(angle)))
        y = int(text_radius * math.sin(math.radians(angle)))
        text = [x - int(w/2), y - int(h/2), int(w), int(h), Qt.AlignCenter, text]
        painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])

    def draw_big_needle_center_point(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 8) - (self.pen.width() / 2)),
                0,
                self.scale_angle_start_value, 360, False)

        grad = QConicalGradient(QPointF(0, 0), 0)

        for eachcolor in self.needle_center_bg:
            grad.setColorAt(eachcolor[0], eachcolor[1])
        painter.setBrush(grad)

        painter.drawPolygon(colored_scale_polygon)

    def draw_outer_circle(self):
        painter = QPainter(self)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 2) - (self.pen.width())),
                (self.widget_diameter / 6),
                self.scale_angle_start_value / 10, 360, False)

        radialGradient = QRadialGradient(QPointF(0, 0), self.width())

        for eachcolor in self.outer_circle_bg:
            radialGradient.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(radialGradient)

        painter.drawPolygon(colored_scale_polygon)

    def draw_needle(self):
        painter = QPainter(self)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.NeedleColor)
        painter.rotate(((self.value - self.value_offset - self.minValue) * self.scale_angle_size /
                        (self.maxValue - self.minValue)) + 90 + self.scale_angle_start_value)

        painter.drawConvexPolygon(self.value_needle[0])

    def resizeEvent(self, event):
        self.rescale_method()
        pass

    def paintEvent(self, event):

        self.draw_outer_circle()
        # Colored pie area
        if self.enable_filled_Polygon:
            self.draw_filled_polygon()

        # Draw scale marker lines
        if self.enable_fine_scaled_marker:
            self.create_fine_scaled_marker()
        if self.enable_big_scaled_marker:
            self.draw_big_scaled_marker()

        # Draw scale marker value text
        if self.enable_scale_text:
            self.create_scale_marker_values_text()

        # Display Value
        if self.enable_value_text:
            self.create_value_text()
            self.create_units_text()

        # Draw needle
        if self.enable_Needle_Polygon:
            self.draw_needle()

        # Draw Center Point
        if self.enable_CenterPoint:
            self.draw_big_needle_center_point()
