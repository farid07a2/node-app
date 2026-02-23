import math
import os

from PySide2.QtCore import QLine
from PySide2.QtGui import QColor, QPen, QPixmap, QBrush, QPainter
from PySide2.QtWidgets import QGraphicsScene


class QDMGraphicsScene (QGraphicsScene):
    def __init__(self,scene,parent=None):
        super().__init__(parent)
        self.scene=scene
        self.grSize=20
        self.gridSquare=5
        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")  # light
        self._color_dark = QColor("#292929")  # Dark light
        #
        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(1)
        #
        # self.scene_width, self.scene_height = 64000, 64000   #creation width /height


        # self.scene_width,self.scene_height=64000,64000

        # self.scene_width, self.scene_height = 100, 100
        # self.setSceneRect(0,0, self.scene_width, self.scene_height)
        # self.setSceneRect(-self.scene_width//2,-self.scene_height//2,self.scene_width,self.scene_height)
        # self.setSceneRect(-self.scene_width // 2, -self.scene_height // 2, self.scene_width, self.scene_height)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(base_dir, "..", "icons", "SCADA.jpg")

        self.bg_pixmap = QPixmap(bg_path)

        # self.setBackgroundBrush(QBrush(pixmap))

        self.setBackgroundBrush(self._color_background)
        # self.selectionChanged.connect(self.onSelectionChanged)

    # def onSelectionChanged(self):
    #     view = self.views()[0]
    #     print("Selection changed")


    def setGrScene(self,width,height):
        self.setSceneRect(-width // 2, -height // 2, width, height)
        # self.setSceneRect(-width, -height, width, height)

    # this for create Grid with x,y coordinate
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # if not self.bg_pixmap.isNull():
        #     # نرسم الصورة بدءًا من أعلى يسار Scene
        #     # painter.drawPixmap(0, 0, self.sceneRect().width()//20, self.sceneRect().height()//20, self.bg_pixmap)
        #     painter.drawPixmap(-self.sceneRect().width(), -self.sceneRect().height(), self.sceneRect().width(), self.sceneRect().height() , self.bg_pixmap)
        # painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

        # here we are create our grid
        left=int (math.floor(rect.left())) #
        right=int (math.floor(rect.right()))
        top = int (math.floor(rect.top()))
        bottom = int (math.floor(rect.bottom()))

        first_left = left - (left % self.grSize)   # first left point after border for draw lines
        first_top = top - (top % self.grSize) # first Top point after border for draw lines

        #     # compute all lines to be drawn
        lines_light, lines_dark = [], []

        for x in range(first_left, right, self.grSize): # step =20 x=first then x=first + grSize
            # if (x % 100 (self.gridSize*self.gridSquares) != 0): lines_light.append(QLine(x, top, x, bottom))
            if x % (self.grSize * self.gridSquare) != 0:
                lines_light.append(QLine(x, top, x, bottom))  # draw point1 (x=first_left,top) and step by 20 px
                                                              # point2 (x=first_left,bottom)
            else:
                lines_dark.append(QLine(x, top, x, bottom))  # add light x Dark
        #
        for y in range(first_top, bottom, self.grSize):
            #         if (y % (self.gridSize*self.gridSquares) != 0):
            if y % (self.grSize * self.gridSquare) != 0:
                lines_light.append(QLine(left, y, right, y)) # draw horizontal line point (left,y)
                # terminate point(right,y)
            # lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))  # add light Y Dark
        #
        #
        # draw the lines
        # use Pen for create lines
        painter.setPen(self._pen_light)
        painter.drawLines(lines_light)  # get all parameter (a1,a2, a3,a3......) list

        painter.setPen(self._pen_dark)
        painter.drawLines(lines_dark)
        # painter.setPen(QPen(QColor("white")))
        # rect.left(), rect.top(), rect.left()+100, rect.top()+100
        # painter.drawLines([QLine(left, top, left+500, top+500)])
        # drw th lines