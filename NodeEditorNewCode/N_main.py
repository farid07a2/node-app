import inspect
import os
import sys


sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..",".."))
from PySide2.QtWidgets import QApplication
from NodeEditorNewCode.node_editor_window import NodeEditorWindow
from NodeEditorNewCode.utils import loadStyleSheet

if __name__=="__main__":
    app=QApplication(sys.argv)
    wnd= NodeEditorWindow()
    wnd.node_editor.addNodes()

    module_path = os.path.dirname(inspect.getfile(wnd.__class__))

    styleSheet_filename = os.path.join(module_path, "qss/nodestyle.qss")

    loadStyleSheet(styleSheet_filename)
    sys.exit(app.exec_())

