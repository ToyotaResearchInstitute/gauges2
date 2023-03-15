from PyQt5.QtWidgets import QLineEdit
from rqt_py_common.topic_completer import TopicCompleter

class TopicQLineEdit(QLineEdit):

    def setNode(self, node):
        self._node = node

    def focusInEvent(self, event):
        completer = self.completer()
        if type(completer) == type(TopicCompleter()):
            completer.update_topics(self._node)
            self.setCompleter(completer)
        else:
            print("The completer of the QLineEdit is not a TopicCompleter object class")
        super(TopicQLineEdit, self).focusInEvent(event)    
