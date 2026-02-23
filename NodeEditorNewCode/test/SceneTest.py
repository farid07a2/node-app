import sys
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PySide2.QtCore import QLine
from PySide2.QtGui import QPen, QColor

class TestScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        # حجم المشهد 500x500
        self.setSceneRect(50, 50, 1000, 1000)
        self.setBackgroundBrush(QColor("#393939"))  # استخدم الخلفية وليس foreground

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        painter.setPen(QPen(QColor("white"), 2))
        # رسم خط قطري
        painter.drawLine(0, 0, 100, 100)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    scene = TestScene()
    view = QGraphicsView(scene)
    view.setWindowTitle("SceneRect Clipping Demo")
    view.resize(400, 300)
    view.show()

    sys.exit(app.exec_())
