

from PySide2.QtCore import Qt, QDataStream, QIODevice
from PySide2.QtGui import QPixmap

from NodeEditorNewCode.N_node_editor_widget import NodeEditorWidget
from NodeEditorNewCode.N_node_node import Node
from NodeEditorNewCode.calculator.app_conf import LISTBOX_MIMETYPE, get_class_from_op_code
from NodeEditorNewCode.calculator.app_node_base import CalcNode
from NodeEditorNewCode.utils import dumpException

DEBUG = True
class CalculatorSubWindow(NodeEditorWidget):

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setTitle()
        self.scene.addHasBeenModifierdListeners(self.setTitle)
        # self.scene.addDragEnterListeners(self.onDragEnter)
        # self.scene.addDropListeners(self.onDrop)

        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)
        self.scene.setNodeClassSelector(self.getNodeClassFromData)

        self._close_event_listeners=[]

    def getNodeClassFromData(self,data):
        if 'op_code' not in data: return Node
        return get_class_from_op_code(data['op_code'])

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())

    def addCloseEventListener(self,callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        if DEBUG:print("CalSubWindow closeEvent")
        for callback in  self._close_event_listeners: callback(self,event)

    # set dragMoveEvent in graphic Scene for worked well
    def onDragEnter(self,event):
        if DEBUG:
            print("CalSubWind :: -onDragEnter")
            print("text: '%s' " % event.mimeData().text())
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            if DEBUG:
                print(" ... denied drag enter event")
            event.setAccepted(False)



    def onDrop(self,event):
        if DEBUG:
            print("CalSubWind :: -onDrop")
            print("text: '%s' " % event.mimeData().text())
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            op_code = dataStream.readInt8()
            text = dataStream.readQString()



            mouse_position = event.pos()
            scene_position =  self.scene.grScene.views()[0].mapToScene(mouse_position)
            if DEBUG: print("got Drop:[%d] '%s'" % (op_code, text),"mouse:",mouse_position,"scene",scene_position)
            #TODO fix me
            # node = Node(self.scene,text,inputs=[1,1],outputs=[2])
            # node = CalcNode(self.scene, op_code, text, inputs=[1, 1], outputs=[2])
            try:
                node = get_class_from_op_code(op_code)(self.scene) # calNode_add class and () create instance

                print("Created node %s" % node.__class__.__name__)

                node.setPos(scene_position.x(),scene_position.y())


                self.scene.history.storeHistory("Created node %s" % node.__class__.__name__)

                # self.scene.addNode(node)
            except Exception as e: dumpException(e)

            event.setDropAction(Qt.MoveAction)
            event.accept()

        else:
            if DEBUG:
                print(".... drop ignored, not request format '%s'" % LISTBOX_MIMETYPE)
            event.ignore()


