from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLineEdit
from NodeEditorNewCode.N_node_content_widget import QDMNodeContentWidget
from NodeEditorNewCode.calculator.app_conf import register_node, OP_NODE_INPUT
from NodeEditorNewCode.calculator.app_node_base import CalcNode, CalcGraphicsNode
from NodeEditorNewCode.utils import dumpException


class CalcInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("1",self)
        # self.edit.setAlignment(Qt.AlignRight)
        self.edit.setAlignment(Qt.AlignLeft)

        self.edit.setObjectName(self.node.content_label_objname)
        # self.edit.setMinimumHeight(40)
        # self.edit.setMaximumHeight(60)
        # self.edit.setStyleSheet("background-color: lightyellow;")

    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self,data,hashmap={}):
        
        res = super().deserialize(data, hashmap)
        try:
            value = res['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)

        return res


@register_node(OP_NODE_INPUT)
class CalcNode_INPUT(CalcNode):
    icon = "icons/in.png"
    op_code = OP_NODE_INPUT
    op_title = "Input"
    content_label_objname = "calc_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])

    def initInnerClasses(self):
        self.content =  CalcInputContent(self)
        self.grNode =  CalcGraphicsNode(self)

