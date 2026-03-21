

from PySide2.QtCore import Qt, QDataStream, QIODevice
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QGraphicsProxyWidget, QMenu, QAction

from NodeEditorNewCode.N_node_edge import EDGE_TYPE_BEZIER, EDGE_TYPE_DIRECT
from NodeEditorNewCode.N_node_editor_widget import NodeEditorWidget
from NodeEditorNewCode.N_node_node import Node
from NodeEditorNewCode.calculator.app_conf import LISTBOX_MIMETYPE, get_class_from_op_code, CALC_NODES
# from NodeEditorNewCode.calculator.app_node_base import CalcNode
from NodeEditorNewCode.utils import dumpException

DEBUG = True
DEBUG_CONTEXT = True
class CalculatorSubWindow(NodeEditorWidget):

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setTitle()
        self.initNewNodeActions()
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

    def contextMenuEvent(self, event):
        try:
            item = self.scene.getItemAt(event.pos())

            if DEBUG_CONTEXT: print(item)

            if type (item) == QGraphicsProxyWidget:
                item = item.widget()

            if hasattr(item,'node') or hasattr(item,'socket'):
                self.handleNodeContextMenu(event)
            elif hasattr(item,'edge'):
                self.handleEdgeContextMenu(event)

            else:
                self.handleNewNodeContextMenu(event)



            return super().contextMenuEvent(event)
        except Exception as e:dumpException(e)

    def handleNodeContextMenu(self,event):
        if DEBUG_CONTEXT : print('Context: Node')
        context_menu = QMenu(self)
        markDirtyAct = context_menu.addAction("Mark Dirty")
        markDirtyDescendantAct = context_menu.addAction("Mark Descendant Dirty")

        markInvalidAct = context_menu.addAction("Mark Invalid")
        unmarkDirtyAct = context_menu.addAction("Unmark Dirty")
        evalAct = context_menu.addAction("Eval")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if type(item) == QGraphicsProxyWidget:
            item = item.widget()
        if hasattr(item, 'node'):
            selected = item.node
        if hasattr(item, 'socket'):
            selected = item.socket.node

        if DEBUG_CONTEXT: print("got item: ", selected)

        if selected and action == markDirtyAct:
            selected.markDirty()

        if selected and action == markDirtyDescendantAct:
            selected.markDescendantDirty()
            

        if selected and action == markInvalidAct:
            selected.markInvalid()

        if selected and action == unmarkDirtyAct:
            selected.markInvalid(False)

        if selected and action == evalAct:
            val = selected.eval()
            if DEBUG_CONTEXT: print("EVALUATION:",val)

    def handleEdgeContextMenu(self,event):
        if DEBUG_CONTEXT : print('Context: Edge')
        context_menu = QMenu(self)
        bezierAct = context_menu.addAction("Bezier Edge")
        directAct = context_menu.addAction("Direct Edge")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if hasattr(item,'edge'):
            selected = item.edge
        if selected and action == bezierAct: selected.edge_type = EDGE_TYPE_BEZIER
        if selected and action == directAct: selected.edge_type = EDGE_TYPE_DIRECT




    def handleNewNodeContextMenu(self,event):
        if DEBUG_CONTEXT : print('Context: Empty Space')

        context_menu = self.initNodesContextMenu()
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        if action is not None:
            new_calc_node = get_class_from_op_code(action.data())(self.scene)
            scene_pos = self.scene.getView().mapToScene(event.pos())
            new_calc_node.setPos(scene_pos.x(),scene_pos.y())
            if DEBUG_CONTEXT: print("Selected Node:",new_calc_node)


    def initNodesContextMenu(self):
        context_menu = QMenu(self)
        keys = list(CALC_NODES.keys())
        keys.sort()
        for key in keys:
            context_menu.addAction(self.node_actions[key])
        return context_menu

    def initNewNodeActions(self):
        self.node_actions = {}
        keys = list(CALC_NODES.keys())
        keys.sort()
        for key in keys :
            node = CALC_NODES[key]
            self.node_actions[node.op_code] = QAction(QIcon(node.icon), node.op_title)
            self.node_actions[node.op_code].setData(node.op_code)