import os.path

from PySide2.QtCore import Qt, QSignalMapper
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QMainWindow, QMdiArea, QWidget, QListWidget, QDockWidget, QAction, QMessageBox, \
    QFileDialog

from NodeEditorNewCode.calculator.app_sub_window import CalculatorSubWindow
from NodeEditorNewCode.node_editor_window import NodeEditorWindow
from NodeEditorNewCode.utils import dumpException, loadStyleSheets

# images for the dark skin
import NodeEditorNewCode.calculator.qss.nodeeditor_dark_resources


class CalculatorWindow(NodeEditorWindow):

    # def __init__(self,parent=None):
    #     super().__init__(parent)
    #
    #     self.initUI()

    def initUI(self):
        self.name_company = 'NameCompany'
        self.name_product = 'Calculator NodeEditor'

        # get dir parent of this file calc_window "__file__" means this file
        self.stylesheet_filename = os.path.join(os.path.dirname(__file__), "qss/nodeeditor.qss")

        loadStyleSheets(os.path.join(os.path.dirname(__file__), "qss/nodeeditor-dark.qss"),
                        self.stylesheet_filename
                        )

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()
        self.createNodesDock()

        self.readSettings()

        self.setWindowTitle("Calculator NodeEditor Example")

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    # def closeEvent(self, event):
    #     # event.accept()
    #     # return
    #     try:
    #         if self.maybeSave():
    #             event.accept()
    #         else:event.ignore()
    #     except Exception as e: dumpException(e)

    # import traceback
    # traceback.print_tb(e.__traceback__)
    # print(e)

    def onFileOpen(self):
        fnames, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file')

        print()
        try:
            for fname in fnames:

                if fname:
                    existing = self.findMidChild(fname)
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        # we need to create new subWindow and open the file
                        nodeeditor = CalculatorSubWindow()

                        if nodeeditor.fileload(fname):
                            self.statusBar().showMessage("File %s loaded " % fname, 5000)
                            nodeeditor.setTitle()
                            subwnd = self.mdiArea.addSubWindow(nodeeditor)
                            subwnd.show()
                        else:
                            nodeeditor.close()

        except Exception as e:
            dumpException(e)
            #     if fname == '':
            #         return
            #
            # if os.path.isfile(fname):
            #     self.getCurrentNodeEditorWidget().scene.loadFromFile(fname)
            #     self.filename = fname
            #     self.setTitle()


    def onFileSave(self):
        current_nodeeditor = self.activeMidChild()
        if current_nodeeditor:
            if not current_nodeeditor.isFilenameSet():
                return self.onFileSaveAs()
            else:
                current_nodeeditor.fileSave() # we don't pass argument,keep the file name
                self.statusBar().showMessage("Successfully saved %s" % current_nodeeditor.filename,5000)
                return True


    def onFileSaveAs(self):
        current_nodeeditor =  self.activeMidChild()
        if current_nodeeditor:
            fname,filter = QFileDialog.getSaveFileName(self,"Save graph file")
            if fname =='':return False
            current_nodeeditor.fileSave(fname)
            current_nodeeditor.setTitle()
            self.statusBar().showMessage("Successfully saved as %s" % fname,5000)
            return True

    def createMenus(self):
        super().createMenus()
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

    def about(self):
        QMessageBox.about(self, "About Calculator NodeEditor Example",
                          "The <b>Calculator NodeEditor</b> example demonstrates how to write multiple "
                          "document interface applications using PyQt5 and NodeEditor. For more information visit: "
                          "<a href='https://www.blenderfreak.com/'>www.BlenderFreak.com</a>")

    def createActions(self):
        super().createActions()

        self.closeAct = QAction("Cl&ose", self, statusTip="Close the active window",
                                triggered=self.mdiArea.closeActiveSubWindow)

        self.closeAllAct = QAction("Close &All", self, statusTip="Close all the windows",
                                   triggered=self.mdiArea.closeAllSubWindows)

        self.tileAct = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)

        self.cascadeAct = QAction("&Cascade", self, statusTip="Cascade the windows",
                                  triggered=self.mdiArea.cascadeSubWindows)

        self.nextAct = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                               statusTip="Move the focus to the next window",
                               triggered=self.mdiArea.activateNextSubWindow)

        self.previousAct = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild,
                                   statusTip="Move the focus to the previous window",
                                   triggered=self.mdiArea.activatePreviousSubWindow)

        self.separatorAct = QAction(self)
        self.separatorAct.setSeparator(True)
        self.aboutAct = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addAction(self.closeAllAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAct)
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)

        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)

    def createToolBars(self):
        pass

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def updateMenus(self):
        pass

    def createNodesDock(self):
        self.listWidget = QListWidget()
        self.listWidget.addItem("Add")
        self.listWidget.addItem("Substract")
        self.listWidget.addItem("Multiply")
        self.listWidget.addItem("Division")
        self.items = QDockWidget("Nodes")
        self.items.setWidget(self.listWidget)
        self.items.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.items)

    def readSettings(self):
        pass

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def onFileNew(self):
        try:
            subwind = self.createMidChild()
            subwind.show()
        except Exception as e:
            dumpException(e)

    def createMidChild(self):
        nodeeditor = CalculatorSubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        return subwnd

    def findMidChild(self,filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None

    def activeMidChild(self):
        """ we're returning NodeEditor ... """

        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None
