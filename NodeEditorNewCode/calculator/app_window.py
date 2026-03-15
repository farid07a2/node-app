import os.path

from PySide2.QtCore import Qt, QSignalMapper
from PySide2.QtGui import QKeySequence, QIcon
from PySide2.QtWidgets import QMainWindow, QMdiArea, QWidget, QListWidget, QDockWidget, QAction, QMessageBox, \
    QFileDialog

from NodeEditorNewCode.calculator.app_conf import register_node, CALC_NODES
from NodeEditorNewCode.calculator.app_conf_nodes import *

from NodeEditorNewCode.calculator.app_drag_listbox import QDMDragListbox
from NodeEditorNewCode.calculator.app_sub_window import CalculatorSubWindow
from NodeEditorNewCode.node_editor_window import NodeEditorWindow
from NodeEditorNewCode.utils import dumpException, loadStyleSheets


# images for the dark skin
import NodeEditorNewCode.calculator.qss.nodeeditor_dark_resources

DEBUG = False
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

        self.empty_icon = QIcon(".")

        if not DEBUG:
            print("register_node")
            print(CALC_NODES)


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

        self.createNodesDock()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()


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
                            # subwnd = self.mdiArea.addSubWindow(nodeeditor)
                            subwnd = self.createMidChild(nodeeditor)

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
    def getCurrentNodeEditorWidget(self):
        # return self.activeMidChild()
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None


    # def onFileSave(self):
    #     current_nodeeditor = self.getCurrentNodeEditorWidget()
    #     if current_nodeeditor:
    #         if not current_nodeeditor.isFilenameSet():
    #             return self.onFileSaveAs()
    #         else:
    #             current_nodeeditor.fileSave() # we don't pass argument,keep the file name
    #             self.statusBar().showMessage("Successfully saved %s" % current_nodeeditor.filename,5000)
    #             current_nodeeditor.setTitle()
    #             return True


    # def onFileSaveAs(self):
    #     current_nodeeditor =  self.activeMidChild()
    #     if current_nodeeditor is not None:
    #         fname,filter = QFileDialog.getSaveFileName(self,"Save graph file")
    #         if fname =='':return False
    #
    #         current_nodeeditor.fileSave(fname)
    #         current_nodeeditor.setTitle()
    #         self.statusBar().showMessage("Successfully saved as %s" % fname,5000)
    #         return True


    def createMenus(self):
        super().createMenus()
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actAbout)

        self.editMenu.aboutToShow.connect(self.updateEditMenu)

    def updateMenus(self):
        active = self.getCurrentNodeEditorWidget()
        hasMidChild = (active is not None)  # return True or False

        self.actSave.setEnabled(hasMidChild)
        self.actSaveAs.setEnabled(hasMidChild)

        self.actClose.setEnabled(hasMidChild)
        self.actCloseAll.setEnabled(hasMidChild)

        self.actTile.setEnabled(hasMidChild)
        self.actCascade.setEnabled(hasMidChild)

        self.actNext.setEnabled(hasMidChild)
        self.actPrevious.setEnabled(hasMidChild)

        self.actSeparator.setVisible(hasMidChild)
        self.updateEditMenu()

    def updateEditMenu(self):
        try:
            if DEBUG:
                print("update Edit menu")
            active = self.getCurrentNodeEditorWidget()
            hasMidChild = (active is not None)  # return True or False
            # TODO: continue here
            self.actPaste.setEnabled(hasMidChild)
            self.actCut.setEnabled(hasMidChild and active.hasSelectedItems())
            self.actCopy.setEnabled(hasMidChild and active.hasSelectedItems())
            self.actDelete.setEnabled(hasMidChild and active.hasSelectedItems())

            self.actUndo.setEnabled(hasMidChild and active.canUndo())
            self.actRedo.setEnabled(hasMidChild and active.canRedo())
        except Exception as e: dumpException(e)


    def updateWindowMenu(self):
        self.windowMenu.clear()

        toolbar_nodes = self.windowMenu.addAction("Nodes Toolbar")
        toolbar_nodes.setCheckable(True)
        toolbar_nodes.triggered.connect(self.onWindowNodesToolbar)
        toolbar_nodes.setCheckable(self.nodesDock.isVisible())
        self.windowMenu.addSeparator()
        
        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.getCurrentNodeEditorWidget())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def onWindowNodesToolbar(self):
        if self.nodesDock.isVisible():
            self.nodesDock.hide()
        else:
            self.nodesDock.show()


    def about(self):
        QMessageBox.about(self, "About Calculator NodeEditor Example",
                          "The <b>Calculator NodeEditor</b> example demonstrates how to write multiple "
                          "document interface applications using PyQt5 and NodeEditor. For more information visit: "
                          "<a href='https://www.blenderfreak.com/'>www.BlenderFreak.com</a>")

    def createActions(self):
        super().createActions()

        self.actClose = QAction("Cl&ose", self, statusTip="Close the active window",
                                triggered=self.mdiArea.closeActiveSubWindow)

        self.actCloseAll = QAction("Close &All", self, statusTip="Close all the windows",
                                   triggered=self.mdiArea.closeAllSubWindows)

        self.actTile = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)

        self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows",
                                  triggered=self.mdiArea.cascadeSubWindows)

        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                               statusTip="Move the focus to the next window",
                               triggered=self.mdiArea.activateNextSubWindow)

        self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild,
                                   statusTip="Move the focus to the previous window",
                                   triggered=self.mdiArea.activatePreviousSubWindow)

        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)
        self.actAbout = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)

    def createToolBars(self):
        pass

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createNodesDock(self):
        # self.nodeslistWidget = QListWidget()
        self.nodeslistWidget = QDMDragListbox()

        self.nodesDock = QDockWidget("Nodes")
        self.nodesDock.setWidget(self.nodeslistWidget)
        self.nodesDock.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.nodesDock)

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

    def createMidChild(self,child_widget=None):
        # nodeeditor = CalculatorSubWindow()
        nodeeditor = child_widget if child_widget is not None else CalculatorSubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        # nodeeditor.scene.addItemSelectedListeners(self.updateEditMenu)
        # nodeeditor.scene.addItemDeselectedListeners(self.updateEditMenu)
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeeditor.addCloseEventListener(self.onSubWindowClose)

        return subwnd

    def onSubWindowClose(self, widget, event):
        existing =  self.findMidChild(widget.filename)
        self.mdiArea.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()
        else:
            event.ignore()


    def findMidChild(self,filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None

    # def activeMidChild(self):
    #     """ we're returning NodeEditor ... """
    #
    #     activeSubWindow = self.mdiArea.activeSubWindow()
    #     if activeSubWindow:
    #         return activeSubWindow.widget()
    #     return None
