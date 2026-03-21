from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QFont, QPainter, QPen, QBrush, QPainterPath, QColor
from PySide2.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsProxyWidget

# from CopyPySideProject.N_node_edge import DEBUG

DEBUG = False
class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node,parent=None):
        super().__init__(parent)
        self.node=node
        self.setZValue(1)
        self.content=self.node.content  # this get By node constructor self.content=QDMNodeContentWidget()

        #init our flags
        self._was_moved = False
        self._last_selected_state = False
        self.initSizes()
        self.initAssets()

        # init title


        self.initUI()



    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable )
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.initTitle()
        self._title = self.node.title

        self.initSocket()
        self.initContent()

    def initSizes(self):
        self.width = 180
        self.height = 240
        self.title_height = 24.0
        self.edge_roundness = 10.0
        self.edge_padding = 10.0
        # self.title_horizontal_padding = 20.0
        self.title_horizontal_padding = 4.0
        self.title_vertical_padding = 4.0

    def initAssets(self):
        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 10)
        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))
        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))


    def onSelected(self):
        if DEBUG:
            print("- grNode onSelected")
        self.node.scene.grScene.itemSelected.emit()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # self.node.updateConnectedEdges()
        # optimize we just update this selected nodes

        # print("Graphic scene is :",type(self.scene()))
        if DEBUG:
            print("list Nodes:",self.scene().scene.nodes)
        for node in self.scene().scene.nodes: # self.scene = QDMGraphicScene
            if DEBUG:
                print("grNode :: Node In scene:",node)
            if node.grNode.isSelected():
                if DEBUG:
                    print("grNode :: is Selected")
                node.updateConnectedEdges()
        self._was_moved = True

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        # handle when grNode moved
        if self._was_moved:
            self._was_moved=False
            self.node.scene.history.storeHistory("Node Moved",setModified=True)

            if DEBUG:
                print(" grNode last state :",self._last_selected_state)
            self.node.scene.resetLastSelectedStates()
            self._last_selected_state = True

            if DEBUG:
                print(" SCN OLD:",self.node.scene._last_selected_items)
                print(" SCN NEW:",self.node.scene.getSelectedItems())
        #we need to store the last selected stats because moving does also select the nodes
        self.node.scene._last_selected_items = self.node.scene.getSelectedItems()

        # now we want to skip storing

        # handle when grNode was clicked on 
        if (self._last_selected_state != self.isSelected()
                or self.node.scene._last_selected_items != self.node.scene.getSelectedItems()):
            self.node.scene.resetLastSelectedStates()
            self._last_selected_state = self.isSelected()
            self.onSelected()


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
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_roundness, self.edge_roundness)
        path_title.addRect(0, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        path_title.addRect(self.width - self.edge_roundness, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(0, self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(self.width - self.edge_roundness, self.title_height, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())
        # outerLine

        path_outline=QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_roundness, self.edge_roundness)
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



    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node= self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self.title_horizontal_padding, 0)
        self.title_item.setTextWidth(self.width - 2 * self.title_horizontal_padding)


    def initSocket(self):
        pass



    def initContent(self):
        self.grContent=QGraphicsProxyWidget(self)

        self.content.setGeometry(self.edge_padding, self.title_height + self.edge_padding,
                                 self.width - 2 * self.edge_padding,
                                 self.height - 2 * self.edge_padding - self.title_height)

        self.grContent.setWidget(self.content)



