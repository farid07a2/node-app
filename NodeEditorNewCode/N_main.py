import inspect
import os
import sys

from PySide2.QtWidgets import QApplication
from N_node_editor_widget import NodeEditorWidget
from NodeEditorNewCode.node_editor_window import NodeEditorWindow
from NodeEditorNewCode.utils import loadStyleSheet

if __name__=="__main__":
    app=QApplication(sys.argv)
    wnd= NodeEditorWindow()

    module_path = os.path.dirname(inspect.getfile(wnd.__class__))

    styleSheet_filename = os.path.join(module_path, "qss/nodestyle.qss")

    loadStyleSheet(styleSheet_filename)
    sys.exit(app.exec_())

