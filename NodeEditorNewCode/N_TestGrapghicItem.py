import os

from PySide2.QtCore import QRectF
from PySide2.QtGui import QPixmap, QPen, QColor, QBrush, QPainterPath, Qt
from PySide2.QtWidgets import QGraphicsItem


class GraphicsTestItem (QGraphicsItem):
    def __init__(self):
        super().__init__()

        self.width = 50
        self.height = 50
        self.edge_size = 10

        base_dir = os.path.dirname(os.path.abspath(__file__))
        # icon_path = os.path.join(base_dir, "..", "icons", "valve.png")
        # self.icon = QPixmap(icon_path)

        self._pen = QPen(QColor("#AAAAAA"), 2)
        self._brush = QBrush(QColor("#2E3A46"))

        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable
        )

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(painter.Antialiasing)

        # جسم المضخة
        path = QPainterPath()
        path.addRoundedRect(
            0, 0,
            self.width,
            self.height,
            self.edge_size,
            self.edge_size
        )

        painter.setPen(self._pen)
        painter.setBrush(self._brush)
        painter.drawPath(path)

        # if not self.icon.isNull():
        #     icon_size = 40
        #     painter.drawPixmap(
        #         (self.width - icon_size) // 2,
        #         (self.height - icon_size) // 2,
        #         icon_size,
        #         icon_size,
        #         self.icon
        #     )
        if self.isSelected():
            painter.setPen(QPen(QColor("#00AEEF"), 2, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(
                0, 0,
                self.width, self.height,
                self.edge_size, self.edge_size
            )