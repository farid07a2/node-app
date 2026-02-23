from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QFont, QPainter, QPen, QBrush, QPainterPath, QColor
from PySide2.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsProxyWidget

# from CopyPySideProject.N_node_edge import DEBUG


class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node,parent=None):
        super().__init__(parent)
        self.node=node
        self.setZValue(1)
        self.content=self.node.content  # this get By node constructor self.content=QDMNodeContentWidget()

        self._title_color=Qt.white
        self._title_font = QFont("Ubuntu",10)
        self._pen_default=QPen(QColor("#7F000000"))
        self._pen_selected=QPen(QColor("#FFFFA637"))
        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background=QBrush(QColor("#E3212121"))


        self.width= 180
        self.height= 240
        self.title_height=24.0
        self.edge_size = 10.0
        self._padding=20.0
        # init title
        self.initTitle()
        self._title = self.node.title

        # init Sockets
        self.initSocket()

        self.initContent()

        self.initUI()
        self.wasMoved = False

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # self.node.updateConnectedEdges()
        # optimize we just update this selected nodes

        # print("Graphic scene is :",type(self.scene()))
        print("list Nodes:",self.scene().scene.nodes)
        for node in self.scene().scene.nodes: # self.scene = QDMGraphicScene
            print("grNode :: Node In scene:",node)
            if node.grNode.isSelected():
                print("grNode :: is Selected")
                node.updateConnectedEdges()
        self.wasMoved = True

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.wasMoved:
            self.wasMoved=False
            self.node.scene.history.storeHistory("Node Moved",setModified=True)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self,title):
        self._title=title
        self.title_item.setPlainText(self._title)


    # يصف حجم وحدود العنصر بالنسبة لنفسه
    def boundingRect(self):
        return QRectF(0, 0, self.width,self.height).normalized()

                      # 2 * self.edge_size+self.width, 2 * self.edge_size+self.height).normalized()

    # ----------------------------------------
    # REQUIRED: How the item is drawn
    # ----------------------------------------
    def paint(self, painter: QPainter, option, widget=None):

        # Node body
        # title
        path_title=QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0,0,self.width,self.title_height,self.edge_size,self.edge_size)
        path_title.addRect(0,self.title_height-self.edge_size,self.edge_size,self.edge_size)
        path_title.addRect(self.width-self.edge_size,self.title_height-self.edge_size,self.edge_size,self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0,self.title_height,self.width,self.height-self.title_height,self.edge_size,self.edge_size)
        path_content.addRect(0,self.title_height,self.edge_size,self.edge_size)
        path_content.addRect(self.width-self.edge_size,self.title_height,self.edge_size,self.edge_size )
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())
        # outerLine

        path_outline=QPainterPath()
        path_outline.addRoundedRect(0,0,self.width,self.height,self.edge_size,self.edge_size)
        # path_outline.addEllipse(-5, 20, 10, 10)
        # path_outline.addEllipse(-5, 60, 10, 10)

        # painter.drawPath(path)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())

        # painter.setPen(QPen(Qt.black, 2))
        # painter.setBrush(QBrush(Qt.darkGray))
        # painter.drawRect(0, 0, self.width, self.height)
        #
        # # Title background
        # painter.setBrush(QBrush(Qt.gray))
        # painter.drawRect(0, 0, self.width, 24)

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable )
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node= self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding,0)
        self.title_item.setTextWidth(self.width- 2 * self._padding)


    def initSocket(self):
        pass



    def initContent(self):
        self.grContent=QGraphicsProxyWidget(self)
        self.content.setGeometry(self.edge_size,self.title_height+self.edge_size,
                                 self.width-2*self.edge_size,
                                 self.height-2*self.edge_size-self.title_height)
        self.grContent.setWidget(self.content)



