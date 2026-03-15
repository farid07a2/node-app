import os

from PySide2.QtCore import QFile
from PySide2.QtGui import QBrush, Qt, QPen, QColor, QFont
from PySide2.QtWidgets import QWidget, QGraphicsView, QBoxLayout, QVBoxLayout, QGraphicsScene, QGraphicsItem, \
    QPushButton, QTextEdit, QApplication, QMessageBox

from NodeEditorNewCode.N_node_edge import Edge, EDGE_TYPE_DIRECT, EDGE_TYPE_BEZIER
from NodeEditorNewCode.N_node_graphics_view import QDMGraphicsView
from NodeEditorNewCode.N_node_node import Node
from NodeEditorNewCode.N_node_scene import Scene, InvalidFile
from NodeEditorNewCode.N_node_socket import Socket


class NodeEditorWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        # self.styleSheet_filename="qss/nodestyle.qss"
        # self.loadStyleSheet(self.styleSheet_filename)

        self.filename = None
        self.initUI()

    def initUI(self):

        # self.setGeometry(200,200,800,500)
        self.layout=QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        # 2- create scene
        self.scene=Scene()
        # self.grScene=self.scene.grScene

        # 1 - Create Graphic view
        self.view=QDMGraphicsView(self.scene.grScene,self)
        # self.view.setScene(self.grScene)
        self.layout.addWidget(self.view)
        # self.addNodes()
        # self.addDebugContent()

        # self.show()

    def isModified(self):
        return self.scene.isModified()

    def isFilenameSet(self):
        return self.filename is not None

    def getSelectedItems(self):
        # return self.scene.grScene.selectedItems()
        return self.scene.getSelectedItems()

    def hasSelectedItems(self):
        return self.getSelectedItems() != []

    def canUndo(self):
        return self.scene.history.canUndo()
    def canRedo(self):
        return self.scene.history.canRedo()


    def getUserFriendlyFilename(self):
        name = os.path.basename(self.filename) if self.isFilenameSet() else "New Graph"
        # TODO: add * has_been_modified logic here
        return name + ("*" if self.isModified() else "")

    def fileNew(self):
        self.scene.clear()
        self.filename = None
        self.scene.history.clear()
        self.scene.history.storeInitialHistoyStamp()

    def fileload(self,filename):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.scene.loadFromFile(filename)
            self.filename = filename
            # clear history
            self.scene.history.clear()
            self.scene.history.storeInitialHistoyStamp()

            return True
        except InvalidFile as e :
            print(e)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self,"Error loading %s" % os.path.basename(filename),str(e))
            return False
        finally:
            QApplication.restoreOverrideCursor()

    def fileSave(self,filename=None):
        # when called with empty parameter, we won't store the filename
        if filename is not None :
            self.filename = filename
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.scene.saveToFile(self.filename)
        QApplication.restoreOverrideCursor()
        return True



    def addNodes(self):
        self.node1 = Node(self.scene, "Node 01",
                         inputs=[0, 0, 0], outputs=[1])
        self.node1.setPos(-350, -250)

        self.node2 = Node(self.scene, "Node 02",
                         inputs=[3, 3, 3], outputs=[1]) # inputs[socket(Node2,0,L_B),
                                                        # socket(Node2,1,L_B),socket(Node2,2,L_B)]
                                                        # output (Socket(node 2,0,R_B) )
        self.node2.setPos(-75, 0)

        self.node3 = Node(self.scene, "Node 03",
                         inputs=[2, 2, 2], outputs=[1])
        self.node3.setPos(200, -150)

        edge1=Edge(self.scene,self.node1.outputs[0],self.node2.inputs[0],type_edge=EDGE_TYPE_BEZIER )

        """ output (Socket(node 2,0,R_B) ) """
        edge2=Edge(self.scene, self.node2.outputs[0], self.node3.inputs[2], type_edge=EDGE_TYPE_BEZIER)
        self.scene.history.storeInitialHistoyStamp()


    def addDebugContent(self):
        greenBrush=QBrush(Qt.green)
        outerlinePen=QPen(Qt.black)
        outerlinePen.setWidth(2)

        rect1 = self.scene.grScene.addRect(-100,-100,80,100,outerlinePen,greenBrush)
        rect2 = self.scene.grScene.addRect(100, 100, 80, 100, outerlinePen, greenBrush)
        rect1.setFlag(QGraphicsItem.ItemIsMovable)
        self.grScene=self.scene.grScene

        text = self.grScene.addText("Hello for this text",QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        # text.setDefaultTextColor(QColor.fromRgb(1.0,1.0,1.0))
        text.setDefaultTextColor(QColor.fromRgbF(1.0,.7,.7))
        widget_button=QPushButton("hello")
        proxy1=self.grScene.addWidget(widget_button)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy1.setPos(-40,-120)

        # text_widget = QTextEdit()
        # proxy2= self.grScene.addWidget(text_widget)
        # proxy2.setFlag(QGraphicsItem.ItemIsMovable)
        # proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        # proxy2.setPos(150,240)

        one_line = self.grScene.addLine(-200,-100,200,100,outerlinePen)
        one_line.setFlag(QGraphicsItem.ItemIsMovable)

    # move to utils
    # def loadStyleSheet(self,file_name):
    #     print("style Loading:",file_name)
    #     file=QFile(file_name)
    #     file.open(QFile.ReadOnly|QFile.Text)
    #     style_sheet=file.readAll()
    #     # QApplication.instance().setStyleSheet(str(style_sheet))
    #     QApplication.instance().setStyleSheet(str(style_sheet, encoding='utf-8'))
