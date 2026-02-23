import inspect
import os.path
import sys

from PySide2.QtWidgets import QApplication, QStyleFactory

from NodeEditorNewCode.calculator.app_window import CalculatorWindow
from NodeEditorNewCode.utils import loadStyleSheet

if __name__ == '__main__':
    app = QApplication(sys.argv)
    print(QStyleFactory.keys())
    app.setStyle('Fusion')

    wnd = CalculatorWindow()


    # module_path = os.path.dirname(inspect.getfile(wnd.__class__))
    #
    # styleSheet_filename = os.path.join(module_path,"qss/nodestyle.qss")
    #
    #
    # loadStyleSheet(styleSheet_filename)

    wnd.show()
    sys.exit(app.exec_())