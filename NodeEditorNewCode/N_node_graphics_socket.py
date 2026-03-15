from PySide2.QtCore import QRectF
from PySide2.QtGui import QColor, QPen, QBrush
from PySide2.QtWidgets import QGraphicsItem

DEBUG = False
class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self,socket=None,socket_type=1):

        super().__init__(socket.node.grNode)
        self.socket=socket
        self.setZValue(2)
        self.radius = 6.0
        self.outline_width = 1.0
        self._colors=[ QColor("#FFFF7700"),
                       QColor("#FF52e220"),
                       QColor("#FFFF56a6"),
                       QColor("#FFa86db1"),
                       QColor("#FFb54747"),
                       QColor("#FFdb2220"),
                       ]
        self._color_background=self._colors[socket_type]

        self._color_outline = QColor("#FF000000")
        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush=QBrush(self._color_background)

    def paint(self, painter, option, widget=...):
        # painting circle
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        #
        painter.drawEllipse(-self.radius,-self.radius,2 * self.radius,2 * self.radius)


    def boundingRect(self):
        # x, y  QRectF( - self.radius - self.outline_width,- self.radius - self.outline_width,
        # الدائرة مرسومة من (-radius, -radius)
        #
        # والإطار يزيد خارج الدائرة


        return QRectF( - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width)
                       )

    def mousePressEvent(self, event):
        if DEBUG:print('socket was clicked')