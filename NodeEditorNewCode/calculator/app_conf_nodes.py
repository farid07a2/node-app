from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLineEdit, QLabel

from NodeEditorNewCode.N_node_content_widget import QDMNodeContentWidget
from NodeEditorNewCode.calculator.app_conf import OP_NODE_ADD, register_node, OP_NODE_SUB, OP_NODE_MUL, OP_NODE_DIV, \
    OP_NODE_INPUT, OP_NODE_OUTPUT
from NodeEditorNewCode.calculator.app_node_base import CalcNode, CalcGraphicsNode
from NodeEditorNewCode.utils import dumpException


@register_node(OP_NODE_ADD)
class CalcNode_Add(CalcNode):
    icon = "icons/add.png"
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = "+"
    content_label_objname = "calc_node_bg"
    # remove this constructor for use parent constructor
    # def __init__(self, scene):
    #     super().__init__(scene, OP_NODE_ADD, "Add", "+")


@register_node(OP_NODE_SUB)
class CalcNode_SUB(CalcNode):

    icon = "icons/sub.png"
    op_code = OP_NODE_SUB
    op_title = "Substraction"
    content_label = "-"
    content_label_objname = "calc_node_bg"

    # def __init__(self, scene):
    #     super().__init__(scene, OP_NODE_SUB, "Substraction", "-")


@register_node(OP_NODE_MUL)
class CalcNode_MUL(CalcNode):
    icon = "icons/mul.png"
    op_code = OP_NODE_MUL
    op_title = "Mul"
    content_label = "*"
    content_label_objname = "calc_node_bg"

    # def __init__(self, scene):
    #     super().__init__(scene, OP_NODE_MUL, "Multiplication", "*")


@register_node(OP_NODE_DIV)
class CalcNode_DIV(CalcNode):
    icon = "icons/divide.png"
    op_code = OP_NODE_DIV
    op_title = "Div"
    content_label = "/"
    content_label_objname = "calc_node_bg"

    # def __init__(self, scene):
    #     super().__init__(scene, OP_NODE_DIV, "Division", "/")


class CalcInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("1",self)
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)
        
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
        self.content =  CalcOutputContent(self)
        self.grNode =  CalcGraphicsNode(self)

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
