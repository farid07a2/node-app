from PySide2.QtCore import QRectF
from PySide2.QtGui import QImage, QPainter
from PySide2.QtWidgets import QLabel

from NodeEditorNewCode.N_node_content_widget import QDMNodeContentWidget
from NodeEditorNewCode.N_node_graphics_node import QDMGraphicsNode
from NodeEditorNewCode.N_node_node import Node
from NodeEditorNewCode.N_node_socket import LEFT_CENTER, RIGHT_CENTER
from NodeEditorNewCode.utils import dumpException


class CalcGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_roundness = 8
        self.edge_padding = 10
        # self.title_horizontal_padding = 8
        # self.title_vertical_padding = 10
        self.title_horizontal_padding = 10
        self.title_vertical_padding = 5

    def initAssets(self):
        super().initAssets()
        self.icons = QImage("icons/status_icons.png")

    def paint(self, painter: QPainter, option, widget=None):
        super().paint(painter,option,widget)
        offset = 24.0

        if self.node.isDirty(): offset = 0.0
        if self.node.isInvalid(): offset = 48.0
        painter.drawImage(
            QRectF(-10,-10,24.0,24.0),
            self.icons,
            QRectF(offset,0,24.0,24.0)
        )


class CalcContent(QDMNodeContentWidget):
    def initUI(self):
        # remove layout and TextEdit and labels and replace with only label empty
        lbl= QLabel(self.node.content_label,self)
        lbl.setObjectName(self.node.content_label_objname)


DEBUG = True
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

        self.value = None
        # it's really important to mark all nodes Dirty by default
        self.markDirty()


    def initInnerClasses(self):
        self.content = CalcContent(self)
        self.grNode = CalcGraphicsNode(self)

    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

    def evalOperation(self,input1,input2):
        return 123


    def evalImplementation(self):
        i1 = self.getInput(0)
        i2 = self.getInput(1)

        if i1 is None or i2 is None:
            self.markInvalid()
            self.markDescendantDirty()
            self.grNode.setToolTip("Connect all inputs")
            return None
        else:
            # val = i1.eval() + i2.eval()
            val = self.evalOperation(i1.eval(), i2.eval())
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.grNode.setToolTip("")

            self.markDescendantDirty()
            self.evalChildren()
            return val

    def eval(self):
        if not self.isDirty() and not self.isInvalid():
            if DEBUG:
                print(" _> returning cached %s value: " % self.__class__.__name__,self.value)
            return self.value
        try:
            # val = 0
            # return self.evalImplementation()
            val =  self.evalImplementation()

            # self.markDirty(False)
            # self.markInvalid(False)
            return val


        except ValueError as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantDirty()

        except Exception as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            dumpException(e)


    def onInputChanged(self,new_edge):
        if DEBUG: print("%s :: onInputChanged" % self.__class__.__name__)

        self.markDirty()
        self.eval()

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self,data,hashmap={},restore_id=False):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized calcNode '%s'" % self.__class__.__name__," res: ",res)
        return res