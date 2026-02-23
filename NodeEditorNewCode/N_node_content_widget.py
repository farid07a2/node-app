from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

from NodeEditorNewCode.N_node_serializable import Serializable


class QDMNodeContentWidget(QWidget,Serializable):
    def __init__(self,node,parent=None):
        super().__init__(parent)
        self.node=node
        self.initUI()


    def initUI(self):
        self.layout=QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.wdg_label=QLabel("Some title")
        self.layout.addWidget(self.wdg_label)
        self.layout.addWidget(QDMTextEdit("Hello"))

    def setEditingFlag(self,value):
        self.node.scene.grScene.views()[0].editingFlag=value # return list of views but we choose the first

    def serialize(self):
        return {}
    def deserialize(self,data,hashmap={}):
        return False


class QDMTextEdit(QTextEdit):

    # def keyPressEvent(self, e):
    #     # print("QDLTextEdit -- KEY PRESS")
    #     super().keyPressEvent(e)

    def focusInEvent(self, e):
        # print("Focus In")
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(e)
    def focusOutEvent(self, e):
        # print("Focus Out")
        self.parentWidget().setEditingFlag(False)  # parent widget in this case is QDMNodeContentWidget
        super().focusOutEvent(e)
