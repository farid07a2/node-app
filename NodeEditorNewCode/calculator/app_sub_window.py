from PySide2.QtCore import Qt
from NodeEditorNewCode.N_node_editor_widget import NodeEditorWidget

class CalculatorSubWindow(NodeEditorWidget):

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setTitle()
        self.scene.addHasBeenModifierdListeners(self.setTitle)

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())
