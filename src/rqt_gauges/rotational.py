import os

from ament_index_python.resources import get_resource
from qt_gui.plugin import Plugin

from .base_widget import BaseWidget


class Rotational(Plugin):

    def __init__(self, context):
        super().__init__(context)
        self.setObjectName('Rotational')

        self._context = context
        self._node = context.node

        _, package_path = get_resource('packages', 'rqt_gauges')
        ui_file = os.path.join(package_path, 'share', 'rqt_gauges', 'resource', 'rotational.ui')
        self._widget = BaseWidget(self._node, 'Rotational_widget', ui_file)

        context.add_widget(self._widget)
