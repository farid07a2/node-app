from PySide2.QtWidgets import QLabel

from NodeEditorNewCode.N_node_content_widget import QDMNodeContentWidget
from NodeEditorNewCode.N_node_graphics_node import QDMGraphicsNode
from NodeEditorNewCode.N_node_node import Node
from NodeEditorNewCode.N_node_socket import LEFT_CENTER, RIGHT_CENTER


class CalcGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_roundness = 8
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10


class CalcContent(QDMNodeContentWidget):
    def initUI(self):
        # remove layout and TextEdit and labels and replace with only label empty
        lbl= QLabel(self.node.content_label,self)
        lbl.setObjectName(self.node.content_label_objname)



class CalcNode(Node):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"

    # first constructor before update parameter
    # def __init__(self, scene,op_code,op_title, content_label="", content_label_objname="calc_label_bg", inputs=[2,2],outputs=[1]):
    #     self.op_code = op_code
    #     self.op_title = op_title
    #     self.content_label = content_label
    #     self.content_label_objname = content_label_objname
    #     super().__init__(scene, self.op_title,inputs, outputs)

    def __init__(self, scene, inputs=[2,2],outputs=[1]):
        # self.op_code = op_code
        # self.op_title = op_title
        # self.content_label = content_label
        # self.content_label_objname = content_label_objname
        super().__init__(scene, self.__class__.op_title,inputs, outputs)


    def initInnerClasses(self):
        self.content = CalcContent(self)
        self.grNode = CalcGraphicsNode(self)

    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self,data,hashmap={},restore_id=False):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized calcNode '%s'" % self.__class__.__name__," res: ",res)
        return res