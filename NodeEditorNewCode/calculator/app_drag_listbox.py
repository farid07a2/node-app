from PySide2.QtCore import QSize, QMimeData, QByteArray, QDataStream, QIODevice, QPoint
from PySide2.QtGui import QPixmap, QIcon, Qt, QDrag
from PySide2.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView

from NodeEditorNewCode.calculator.app_conf import OP_NODE_INPUT, OP_NODE_OUTPUT, LISTBOX_MIMETYPE, OP_NODE_ADD, \
    OP_NODE_SUB, OP_NODE_MUL, OP_NODE_DIV, CALC_NODES, get_class_from_op_code
from NodeEditorNewCode.utils import dumpException

DEBUG = True
class QDMDragListbox(QListWidget):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.initUI()


    def initUI(self):
        self.setIconSize(QSize(32,32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)

        self.addMyItems()
        # self.nodeslistWidget.addItem("Add")
        # self.nodeslistWidget.addItem("Substract")
        # self.nodeslistWidget.addItem("Multiply")
        # self.nodeslistWidget.addItem("Division")

    def addMyItems(self):
        keys = list(CALC_NODES.keys())
        keys.sort()
        for key in keys:
            node = get_class_from_op_code(key)

            self.addMyItem(node.op_title,node.icon,node.op_code)


        # change by for loop and get node by class
        # self.addMyItem("Input","icons/in.png",OP_NODE_INPUT)
        # self.addMyItem("Output","icons/out.png",OP_NODE_OUTPUT)
        # self.addMyItem("Add","icons/add.png",OP_NODE_ADD)
        # self.addMyItem("Substract","icons/sub.png",OP_NODE_SUB)
        # self.addMyItem("Multiply","icons/mul.png",OP_NODE_MUL)
        # self.addMyItem("Divide","icons/divide.png",OP_NODE_DIV)


    def addMyItem(self,name,icon=None,op_code=0):
        item = QListWidgetItem(name,self) # can be (icon,text,parent, <int>type)
        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(32,32))
        item.setFlags(Qt.ItemIsEnabled| Qt.ItemIsSelectable|Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole,pixmap)
        item.setData(Qt.UserRole + 1,op_code)

    def startDrag(self, *args,**kwargs):
        if DEBUG: print("listBox::startDrag")
        try:
            item=self.currentItem()
            op_code = item.data(Qt.UserRole+1)
            if DEBUG:
                print("dragging item<%d>" % op_code,item)

            pixmap = QPixmap(item.data(Qt.UserRole))

            itemData = QByteArray()
            dataStream = QDataStream(itemData,QIODevice.WriteOnly)
            dataStream << pixmap
            dataStream.writeInt8(op_code)
            dataStream.writeQString(item.text())

            mimeData = QMimeData()
            mimeData.setData(LISTBOX_MIMETYPE,itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width()/2,pixmap.height()/2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)
        except Exception as e: dumpException(e)


