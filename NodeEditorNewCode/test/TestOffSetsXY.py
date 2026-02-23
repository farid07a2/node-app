import sys
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PySide2.QtCore import QLine, Qt
from PySide2.QtGui import QPen, QColor

class TestScene(QGraphicsScene):
    def __init__(self, x_offset=0, y_offset=0):
        super().__init__()
        # المشهد يبدأ من (x_offset, y_offset) وحجمه 500x500
        self.setSceneRect(x_offset, y_offset, 500, 500)
        self.setBackgroundBrush(QColor("#393939"))

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        painter.setPen(QPen(QColor("white"), 3))

        # نرسم خط يمتد من 0,0 → 400,400
        painter.drawLine(0, 0, 400, 400)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # جرب تغيّر x_offset و y_offset
    scene = TestScene(x_offset=250, y_offset=250)  # هنا الخط سيظهر كامل
    # scene = TestScene(x_offset=50, y_offset=50)  # هنا الخط يبدأ خارج المشهد ولن يظهر من البداية

    view = QGraphicsView(scene)
    view.setWindowTitle("SceneRect Offset Demo")
    view.resize(500, 500)
    view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    view.show()

    sys.exit(app.exec_())
