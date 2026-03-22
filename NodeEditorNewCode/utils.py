import traceback

from PySide2.QtCore import QFile
from PySide2.QtWidgets import QApplication


def dumpException(e):
    print("EXCEPTION: %s " % e.__class__.__name__, e)
    traceback.print_tb(e.__traceback__)


def loadStyleSheet(file_name):
    print("style Loading:", file_name)
    file = QFile(file_name)
    file.open(QFile.ReadOnly | QFile.Text)
    style_sheet = file.readAll()
    # QApplication.instance().setStyleSheet(str(style_sheet))
    QApplication.instance().setStyleSheet(str(style_sheet, encoding='utf-8'))


def loadStyleSheets( *args):
    res = ''
    for arg in args:
        file = QFile(arg)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        res += "\n"+str(stylesheet,encoding='utf-8')
    QApplication.instance().setStyleSheet(res)
