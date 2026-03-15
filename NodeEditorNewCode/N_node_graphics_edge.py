import math

from PySide2.QtCore import QPointF
from PySide2.QtGui import QColor, QPen, Qt, QPainterPath
from PySide2.QtWidgets import QGraphicsPathItem, QGraphicsItem

from NodeEditorNewCode.N_node_socket import LEFT_BOTTOM, LEFT_TOP, RIGHT_TOP, RIGHT_BOTTOM

# from node_socket import RIGHT_TOP, RIGHT_BOTTOM

EDGE_CP_ROUNDNESS = 100

DEBUG = False
class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.edge = edge

        # init our flags
        self._last_selected_state = False
        # init our variables
        self.posSource = [0, 0]
        self.posDestination = [200, 100]

        self.initAssets()
        self.initUI()

    def initUI(self):
        self.setFlags(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

    def initAssets(self):
        self._color = QColor("#001000")
        self._color_selected = QColor("#00ff00")
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen_dragging = QPen(self._color)
        self._pen_dragging.setStyle(Qt.DashLine)
        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)
        self._pen_dragging.setWidthF(2.0)

    def onSelected(self):
        if DEBUG:
            print("- grEdge onSelected")
        self.edge.scene.grScene.itemSelected.emit()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self._last_selected_state != self.isSelected():
            self.edge.scene.resetLastSelectedStates()
            self._last_selected_state = self.isSelected()
            self.onSelected()


    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def boundingRect(self):
        return self.shape().boundingRect()

    def shape(self):
        return self.calcPath()

    def paint(self, painter, QStyleOptionGraphicsItem, vidget=None):
        self.setPath(self.calcPath())

        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen if not self.isSelected() else self._pen_selected)

        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def intersectsWith(self,p1,p2):
        cut_path = QPainterPath(p1)
        cut_path.lineTo(p2)
        path = self.calcPath()
        return cut_path.intersects(path)

    def calcPath(self):
        """whene handle drawing QpainterPath from point A to B"""

        raise NotImplemented("this methode hase to be overriden in a child class")


class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def calcPath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        return path


class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def calcPath(self):
        # use by ChatGpt when cut edge
        # if self.edge is None or \
        #         self.edge.start_socket is None or \
        #         self.edge.end_socket is None:
        #     return QPainterPath()

        # try:

        # if not self.edge:
        #     return QPainterPath()

        s = self.posSource
        d = self.posDestination

        dist = (d[0] - s[0]) * 0.5

        # if  s[0]  > d[0] : dist=-1

        cpx_s = +dist
        cpx_d = -dist
        cpy_s = 0
        cpy_d = 0

        # print("ss:",self.edge.start_socket)
        if self.edge.start_socket is not None:
            sspos = self.edge.start_socket.position
            # add relation between sockets input input
            if (s[0] > d[0] and sspos in (RIGHT_TOP, RIGHT_BOTTOM) or (s[0] < d[0] and sspos in (LEFT_TOP, LEFT_TOP))):
                cpx_d *= -1
                cpy_s *= -1

                cpy_d = ((s[1] - d[1]) / math.fabs((s[1] - d[1]) if (s[1] - d[1]) != 0 else 0.00001)
                         ) * EDGE_CP_ROUNDNESS
                cpy_s = ((d[1] - s[1]) / math.fabs((d[1] - s[1]) if (d[1] - s[1]) != 0 else 0.00001)
                         ) * EDGE_CP_ROUNDNESS

        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        # path.lineTo(self.posDestination[0], self.posDestination[1])
        # path.cubicTo( s[0] + dist,s[1],d[0] - dist, d[1]
        path.cubicTo(s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d
                     , self.posDestination[0], self.posDestination[1])
        # self.setPath(path)
        return path
        # s=self.posSource
        # d=self.posDestination
        # dist= (d[0]-s[0])*0.5
        # # if s[0] > d[0]: dist *= -1
        #
        # cpx_s= +dist
        # cpx_d= -dist
        #
        # cpy_s = 0
        # cpy_d = 0
        # sspos = self.edge.start_socket.position # sspos = startSocketPosition
        #
        # if(s[0]>d[0] and sspos in (RIGHT_TOP,RIGHT_BOTTOM) or
        #         ( s[0] < d[0] and sspos in (LEFT_BOTTOM,LEFT_TOP))):
        #     cpx_s *= -1
        #     cpx_d *=-1
        #     cpy_d = (
        #                 (s[1] - d[1]) / math.fabs(
        #                 (s[1] - d[1]) if (s[1] - d[1] !=0 ) else 0.00001 )
        #             )*EDGE_CP_ROUNDNESS
        #
        #     cpy_s = (
        #                     (d[1] - s[1]) / math.fabs(
        #                 (d[1] - s[1]) if (d[1] - s[1] != 0) else 0.00001)
        #             ) * EDGE_CP_ROUNDNESS
        #
        # path=QPainterPath(QPointF(self.posSource[0],self.posSource[1]))
        # # path.cubicTo(s[0]+dist,s[1],d[0]+dist,d[1],self.posDestination[0],self.posDestination[1] )
        # # path.cubicTo(s[0] + dist, s[1],# Control Point1
        # #              d[0] - dist, d[1],# CP2
        # #              self.posDestination[0],self.posDestination[1] # Epoint
        # #              )
        #
        # path.cubicTo(s[0] + cpx_s, s[1]+cpy_s,  # Control Point1
        #              d[0] +cpx_d ,d[1]+cpy_d,  # CP2
        #              self.posDestination[0], self.posDestination[1]  # Epoint
        #              )
        #
        # self.setPath(path)

