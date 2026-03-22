from NodeEditorNewCode.calculator.app_conf import OP_NODE_ADD, register_node, OP_NODE_SUB, OP_NODE_MUL, OP_NODE_DIV
from NodeEditorNewCode.calculator.app_node_base import CalcNode

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


    def evalOperation(self,input1,input2):
        return input1 + input2

    # def evalImplementation(self):
        # self.markInvalid(False)
        # self.markDirty(False)
        # i1=self.getInput(0)
        # i2=self.getInput(1)
        #
        # if not i1 or not i2:
        #     self.markInvalid()
        #     self.markDescendantDirty()
        #     self.grNode.setToolTip("Connect all inputs")
        #     return None
        # else:
        #     val = i1.eval() + i2.eval()
        #     self.value = val
        #     self.markDirty(False)
        #     self.markInvalid(False)
        #     self.grNode.setToolTip("")
        #
        #     self.markDescendantDirty()
        #     self.evalChildren()
        #     return val
        # pass

        # return 123


@register_node(OP_NODE_SUB)
class CalcNode_SUB(CalcNode):

    icon = "icons/sub.png"
    op_code = OP_NODE_SUB
    op_title = "Substraction"
    content_label = "-"
    content_label_objname = "calc_node_bg"

    # def __init__(self, scene):
    #     super().__init__(scene, OP_NODE_SUB, "Substraction", "-")

    def evalOperation(self,input1,input2):
        return input1 - input2


@register_node(OP_NODE_MUL)
class CalcNode_MUL(CalcNode):
    icon = "icons/mul.png"
    op_code = OP_NODE_MUL
    op_title = "Mul"
    content_label = "*"
    content_label_objname = "calc_node_bg"

    # def __init__(self, scene):
    #     super().__init__(scene, OP_NODE_MUL, "Multiplication", "*")

    def evalOperation(self,input1,input2):
        return input1 * input2

@register_node(OP_NODE_DIV)
class CalcNode_DIV(CalcNode):
    icon = "icons/divide.png"
    op_code = OP_NODE_DIV
    op_title = "Div"
    content_label = "/"
    content_label_objname = "calc_node_bg"

    # def __init__(self, scene):
    #     super().__init__(scene, OP_NODE_DIV, "Division", "/")
    def evalOperation(self,input1,input2):
        return input1 / input2