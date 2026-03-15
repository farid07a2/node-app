from PySide2.QtCore import QEvent, Signal
from PySide2.QtGui import QPainter, Qt, QMouseEvent
from PySide2.QtWidgets import QGraphicsView, QApplication

from NodeEditorNewCode.N_node_edge import Edge, EDGE_TYPE_BEZIER
from NodeEditorNewCode.N_node_graphics_cutline import QDMCutLine
from NodeEditorNewCode.N_node_graphics_edge import QDMGraphicsEdge
from NodeEditorNewCode.N_node_graphics_socket import QDMGraphicsSocket

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT=3
EDGE_DRAG_START_THRESHOLD = 10
DEBUG =False

class QDMGraphicsView(QGraphicsView):
    scenePosChanged = Signal(int,int)
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)
        self.mode = MODE_NOOP
        self.editingFlag=False # before edit in item
        self.rubberBandDraggingRectangle = False
        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

        #cutline
        self.cutline = QDMCutLine()
        self.grScene.addItem(self.cutline)



        # self.setDragMode(QGraphicsView.RubberBandDrag) # possibility to select items


    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        self.setDragMode(QGraphicsView.RubberBandDrag)

        # enable dropping
        self.setAcceptDrops(True)

        # listeners
        self._drag_enter_listeners = []
        self._drop_listeners = []


    # def dragEnableEvent(self,event):
    #     for callback in self._drag_enter_listeners: callback()
    #
    #
    # def dropEvent(self,event):
    #     for callback in self._drop_listeners: callback()
    #
    # def addDragEnterListener(self,callback):
    #     self._drag_enter_listeners.append(callback)
    #
    # def addDropListener(self,callback):
    #     self._drop_listeners.append(callback)

    def dragEnterEvent(self, event):
        for callback in self._drag_enter_listeners: callback(event)

    def dropEvent(self, event):
        for callback in self._drop_listeners: callback(event)

    def addDragEnterListener(self, callback):
        self._drag_enter_listeners.append(callback)

    def addDropListener(self, callback):
        self._drop_listeners.append(callback)


    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)


    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def leftMouseButtonPress(self, event):

        item = self.getItemAtClick(event)
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())
        # print("item get by clicked: leftMP ", item)
        # logic
        if DEBUG: print("LMB Click on:", item,self.debug_modifiers(event))
        if hasattr(item,"node") or isinstance(item,QDMGraphicsEdge) or item is None:
            if event.modifiers()  & Qt.ShiftModifier:

                event.ignore()
                fakeEvent= QMouseEvent(QEvent.MouseButtonPress,event.localPos(),event.screenPos(),
                                       Qt.LeftButton,event.buttons() & Qt.LeftButton,
                                       event.modifiers()| Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return

        if type(item) is QDMGraphicsSocket:
            # print("in leftMouseButtonPress Method")
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item,event)
            if res: return

        if item is None:
            if event.modifiers() & Qt.ControlModifier:
                self.mode = MODE_EDGE_CUT
                if DEBUG: print("I ma in MODE_EDGE_CUT")
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease,event.localPos(),event.screenPos(),
                                            Qt.LeftButton,Qt.NoButton,event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return
            else:
                self.rubberBandDraggingRectangle =True

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        # get item which we release mouse button on
        item = self.getItemAtClick(event)

        # logic
        if hasattr(item, "node") or isinstance(item,QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                if DEBUG: print("LMB Realse+ shift on:", item)
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return

        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item,event)
                if res: return

        if self.mode == MODE_EDGE_CUT:
            self.cutIntersectingEdges()
            self.cutline.line_points=[]
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.mode= MODE_NOOP
            return

        # if self.dragMode() == QGraphicsView.RubberBandDrag:
        if self.rubberBandDraggingRectangle:
            self.rubberBandDraggingRectangle = False
            # self.grScene.scene.history.storeHistory("Selection changed")
            # print(">> Selection change")
            current_selected_items = self.grScene.selectedItems()
            if current_selected_items != self.grScene.scene._last_selected_items:

                if current_selected_items == []:
                    self.grScene.itemDeselected.emit()
                else:
                    self.grScene.itemSelected.emit()

                self.grScene.scene._last_selected_items = current_selected_items
                # print(current_selected_items)

            return

        # otherwise deselect everything
        if item is None:
            self.grScene.itemDeselected.emit()


        super().mouseReleaseEvent(event)

    def findSocketAt(self, event):
        pos = self.mapToScene(event.pos())
        for item in self.grScene.items(pos):
            if isinstance(item, QDMGraphicsSocket):
                return item.socket
        return None

    def cutIntersectingEdges(self):
        for ix in range (len(self.cutline.line_points)-1):
            p1 = self.cutline.line_points[ix]
            p2 = self.cutline.line_points[ix+1]

            for edge in self.grScene.scene.edges:
                if edge.grEdge.intersectsWith(p1,p2):
                    edge.remove()
        self.grScene.scene.history.storeHistory("Delete cutted edges",setModified=True)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

        item =self.getItemAtClick(event)
        if DEBUG:
            if isinstance(item,QDMGraphicsEdge) :  print("RMB DEBUG : ", item.edge , "connecting sockets :",
                                                   item.edge.start_socket,"<-->" , item.edge.end_socket)
            if type(item) is QDMGraphicsSocket : print("RMB DEBUG : ", item.socket, "has edges : " ,item.socket.edges)

            if item is None:
                    if DEBUG:
                        print('SCENE:')
                        print('  Nodes:')
                    #list Nodes
                    for node in self.grScene.scene.nodes: print('    ', node)
                    if DEBUG:
                        print('  Edges:')
                    #list Edges
                    for edge in self.grScene.scene.edges: print('    ', edge)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self,event):
        if self.mode==MODE_EDGE_DRAG:
            pos=self.mapToScene(event.pos())
            self.drag_edge.grEdge.setDestination(pos.x(), pos.y())
            self.drag_edge.grEdge.update()

        if self.mode==MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos())
            self.cutline.line_points.append(pos)
            self.cutline.update()

        self.last_scene_mouse_position = self.mapToScene(event.pos())
        self.scenePosChanged.emit(
            int(self.last_scene_mouse_position.x()),int(self.last_scene_mouse_position.y())
        )
        super().mouseMoveEvent(event)

    def keyPressEvent(self,event):
        if event.modifiers() & Qt.ControlModifier:

            # Ctrl + +
            if event.key() in (Qt.Key_Plus, Qt.Key_Equal):
                self.zoomView(self.zoomInFactor)
                return

            # Ctrl + -
            elif event.key() == Qt.Key_Minus:
                self.zoomView(1 / self.zoomInFactor)
                return

        # print('grView:: Key press')

        # if event.key() == Qt.Key_Delete:
        #     if not self.editingFlag:
        #         # print("clic button delete")
        #         self.deleteSelected() # delete node and edge
        #     else:
        #         super().keyPressEvent(event)
        #
        # elif event.key()==Qt.Key_S and event.modifiers() & Qt.ControlModifier:
        #     self.grScene.scene.saveToFile("graph.json")
        # elif event.key()==Qt.Key_L and event.modifiers() & Qt.ControlModifier:
        #     self.grScene.scene.loadFromFile("graph.json")
        # elif event.key() == Qt.Key_1:
        #     self.grScene.scene.history.storeHistory("Item A")
        # elif event.key() == Qt.Key_2:
        #     self.grScene.scene.history.storeHistory("Item B")
        # elif event.key() == Qt.Key_3:
        #     self.grScene.scene.history.storeHistory("Item C")

        #
        # elif (event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier
        #       and not event.modifiers() & Qt.ShiftModifier):
        #     self.grScene.scene.history.undo()
        # elif (event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier
        #       and event.modifiers() & Qt.ShiftModifier):
        #     self.grScene.scene.history.redo()
        #
        # elif event.key() == Qt.Key_H:
        #     print("HISTORY:   len(%d)" % len(self.grScene.scene.history.history_stack) ,
        #           " ---- current_step ",self.grScene.scene.history.history_current_step)
        #     ix=0
        #     for item in self.grScene.scene.history.history_stack:
        #         print("# ",ix,"--",item['desc'])
        #         ix +=1
        #
        #     print(self.grScene.scene.history.history_stack)
        #
        # else:
        super().keyPressEvent(event)

    def zoomView(self, zoomFactor):
        self.zoom += self.zoomStep if zoomFactor > 1 else -self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]:
            self.zoom, clamped = self.zoomRange[1], True

        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)

    def deleteSelected(self):
        if DEBUG: print("List Item selected for removing:",self.grScene.selectedItems())
        for item in self.grScene.selectedItems():

            if isinstance(item, QDMGraphicsEdge):
                item.edge.remove()  # delete
            elif hasattr(item , 'node'):
                item.node.remove()
        self.grScene.scene.history.storeHistory("Delete selected",setModified=True)

    def debug_modifiers(self,event):
        out="MODS: "
        if event.modifiers() & Qt.ShiftModifier: out +="SHIFT"
        if event.modifiers() & Qt.ControlModifier: out +="CTRL"
        if event.modifiers() & Qt.AltModifier: out +="ALT"
        return out


    def getItemAtClick(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):
        if DEBUG: print('View::edgeDragStart - start dragging edge....')
        if DEBUG:print('View::edgeDragStart - assign Start socket to :',item.socket)
        # self.previousEdge = item.socket.edge

        self.drag_start_socket = item.socket
        self.drag_edge=Edge(self.grScene.scene, item.socket, None, EDGE_TYPE_BEZIER)

        # self.dragEdge = Edge(self.grScene.scene, item.socket, self.grScene.scene.nodes[1].outputs[0], EDGE_TYPE_BEZIER)
        if DEBUG:
            print('View :: edgeDragStart - dragEdge: ', self.drag_edge)


    def edgeDragEnd(self, item,event):
        """ return True if skip the rest of the code """
        """ return True if skip the rest of the code """

        socket = None

        if isinstance(item, QDMGraphicsSocket):
            socket = item.socket
        else:
            socket = self.findSocketAt(event)


        self.mode = MODE_NOOP
        # if type(item) is QDMGraphicsSocket:
        if DEBUG:print("View:: edgeDragEnd - End dragging edge")
        self.drag_edge.remove()
        self.drag_edge = None

        if socket:
            if socket != self.drag_start_socket:
                # if we released dragging on socket (other then begining socket)
                # if DEBUG:
                #     print('View::edgeDragEnd previous edge', socket)

                # if socket.hasEdge():
                #     socket.edge.remove()

                # replace with socket.removeAllEdges()
                # for edge in socket.edges:
                #     if DEBUG: print("View :: edgeDragEnd - cleanup edges IN target:",edge)
                #     edge.remove()
                #     if DEBUG: print("View::edgeDragEnd - cleanup edges IN Target",edge,"Removed...")
                #
                if not socket.is_multi_edges:
                    socket.removeAllEdges()
                if not self.drag_start_socket.is_multi_edges:
                    socket.removeAllEdges()

                # if DEBUG:
                #     print('View::edgeDragEnd assign End Socket',socket)
                # if self.previousEdge is not None: self.previousEdge.remove()
                # if DEBUG:
                #     print("View::edgeDragEnd - previous edge removed")
                # self.drag_edge.start_socket=self.drag_start_socket
                # self.drag_edge.end_socket = socket
                # self.drag_edge.start_socket.addEdge(self.drag_edge)
                # self.drag_edge.end_socket.addEdge(self.drag_edge)
                # self.drag_edge.updatePositions()
                #

                new_edge =  Edge(self.grScene.scene,self.drag_start_socket,socket,type_edge=EDGE_TYPE_BEZIER)
                if DEBUG: print("View::edgeDragEnd - created new edge:",new_edge," connecting",new_edge.start_socket,"<-->",new_edge.end_socket)
                self.grScene.scene.history.storeHistory("created new edge by dragging",setModified=True)
                return True

        if DEBUG: print('View::edgeDragEnd end Dragging Edge')
        # self.drag_edge.remove()
        # self.drag_edge = None
        # if DEBUG: print("View::edgeDragEnd => about to set socket to previous edge:",self.previousEdge)
        # if self.previousEdge is not None:
        #     self.previousEdge.start_socket.edge=self.previousEdge

        if DEBUG: print("View::edgeDragEnd everyThing done.")
        return False


    def distanceBetweenClickAndReleaseIsOff(self, event):
        """ measures if we are too far from the last LMB click scene position """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y()) > edge_drag_threshold_sq



    def wheelEvent(self, event):
        # calculate our zoom Factor
        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)
