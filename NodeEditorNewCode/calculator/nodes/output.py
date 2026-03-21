from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel

from NodeEditorNewCode.N_node_content_widget import QDMNodeContentWidget
from NodeEditorNewCode.calculator.app_conf import register_node, OP_NODE_OUTPUT
from NodeEditorNewCode.calculator.app_node_base import CalcNode, CalcGraphicsNode


class CalcOutputContent(QDMNodeContentWidget):
    def initUI(self):
        self.lbl = QLabel("42",self)
        self.lbl.setAlignment(Qt.AlignLeft)
        self.lbl.setObjectName(self.node.content_label_objname)


@register_node(OP_NODE_OUTPUT)
class CalcNode_OUTPUT(CalcNode):
    icon = "icons/out.png"
    op_code = OP_NODE_OUTPUT
    op_title = "Output"
    content_label_objname = "calc_node_output"


    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])

    def initInnerClasses(self):
        self.content = CalcOutputContent(self)
        self.grNode = CalcGraphicsNode(self)


# Way how to register by function call
# register_node(OP_NODE_ADD,CalcNode_Add)
