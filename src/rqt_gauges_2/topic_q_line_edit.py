from PyQt5.QtWidgets import QLineEdit
from rqt_py_common.topic_completer import TopicCompleter


class TopicQLineEdit(QLineEdit):
    # Extension of QLineEdit in order to use the focusIn event from the class.
    # The method is used to update the topics each time the object is focused.

    def setNode(self, node):
        self._node = node

    def focusInEvent(self, event):
        completer = self.completer()
        if isinstance(completer, TopicCompleter):
            completer.update_topics(self._node)
            self.setCompleter(completer)
        else:
            print('The completer of the QLineEdit is not a TopicCompleter object class')
        super().focusInEvent(event)
