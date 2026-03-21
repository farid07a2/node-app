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