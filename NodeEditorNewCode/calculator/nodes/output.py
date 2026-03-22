from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel

from NodeEditorNewCode.N_node_content_widget import QDMNodeContentWidget
from NodeEditorNewCode.calculator.app_conf import register_node, OP_NODE_OUTPUT
from NodeEditorNewCode.calculator.app_node_base import CalcNode, CalcGraphicsNode


class CalcOutputContent(QDMNodeContentWidget):
    def initUI(self):
        self.lbl = QLabel("result",self)
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

    def evalImplementation(self):
        input_node = self.getInput(0)
        if not input_node:
            self.grNode.setToolTip("Input is Not Connected ")
            self.markInvalid()
            return


        val = input_node.eval()
        if val is None:
            self.grNode.setToolTip("Input is NaN ")
            self.markInvalid()
            return


        self.content.lbl.setText("%d" % val)
        self.markDirty(False)
        self.markInvalid(False)

        self.grNode.setToolTip("")
        return val

# Way how to register by function call
# register_node(OP_NODE_ADD,CalcNode_Add)
