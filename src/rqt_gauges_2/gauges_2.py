from python_qt_binding.QtWidgets import QVBoxLayout, QWidget
from qt_gui.plugin import Plugin
from qt_gui_py_common.simple_settings_dialog import SimpleSettingsDialog

class Gauges2(Plugin):

    def __init__(self, context):
        super(Gauges2, self).__init__(context)
        self.setObjectName('Gauges2')

        self._context = context
        self._console_widget = None
        self._widget = QWidget()
        self._widget.setLayout(QVBoxLayout())
        self._widget.layout().setContentsMargins(0, 0, 0, 0)
        if context.serial_number() > 1:
            self._widget.setWindowTitle(
                self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        self._context.add_widget(self._widget)

    def shutdown_console_widget(self):
        if self._console_widget is not None and hasattr(self._console_widget, 'shutdown'):
            self._console_widget.shutdown()

    def shutdown_plugin(self):
        self.shutdown_console_widget()
