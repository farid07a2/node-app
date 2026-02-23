import json
import os.path

from PySide2.QtCore import QSettings, QPoint, QSize
from PySide2.QtWidgets import QMainWindow, QAction, QFileDialog, QLabel, QApplication, QMessageBox

from NodeEditorNewCode.N_node_editor_widget import NodeEditorWidget


class NodeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.name_company = 'CompanyPLC'
        self.name_product = 'PlcManager'
        # deplace to NodeEditorWidget class
        # self.filename = None
        self.initUI()

        # QApplication.instance().clipboard().dataChanged.connect(self.onClipboardChanged)
        # self.cb = QApplication.clipboard()
        # print(self.cb)
        # self.cb.dataChanged.connect(self.onClipboardChanged)
        # self.cb.changed.connect(self.onClipboardChanged)
        # self.cb.selectionChanged.connect(self.onClipboardChanged)

    # def onClipboardChanged(self):
    #     # clip =  QApplication.clipboard()
    # self.cb
    #     print("clipboard changed",self.cb.text())

    # def createAction(self,name,shortcut,tooltip,callback):
    #     act = QAction(name, self)
    #     act.setShortcut(shortcut)
    #     act.setToolTip(tooltip)
    #     act.triggered.connect(callback)
    #     return act

    def createActions(self):
        self.actNew = QAction('&New', self, shortcut='Ctrl+N', statusTip="Create new graph", triggered=self.onFileNew)
        self.actOpen = QAction('&Open', self, shortcut='Ctrl+O', statusTip="Open file", triggered=self.onFileOpen)
        self.actSave = QAction('&Save', self, shortcut='Ctrl+S', statusTip="Save file", triggered=self.onFileSave)
        self.actSaveAs = QAction('Save &As...', self, shortcut='Ctrl+Shift+S', statusTip="Save file as...",
                                 triggered=self.onFileSaveAs)
        self.actExit = QAction('E&xit', self, shortcut='Ctrl+Q', statusTip="Exit application", triggered=self.close)

        self.actUndo = QAction('&Undo', self, shortcut='Ctrl+Z', statusTip="Undo last operation",
                               triggered=self.onEditUndo)
        self.actRedo = QAction('&Redo', self, shortcut='Ctrl+Shift+Z', statusTip="Redo last operation",
                               triggered=self.onEditRedo)
        self.actCut = QAction('Cu&t', self, shortcut='Ctrl+X', statusTip="Cut to clipboard", triggered=self.onEditCut)
        self.actCopy = QAction('&Copy', self, shortcut='Ctrl+C', statusTip="Copy to clipboard",
                               triggered=self.onEditCopy)
        self.actPaste = QAction('&Paste', self, shortcut='Ctrl+V', statusTip="Paste from clipboard",
                                triggered=self.onEditPaste)
        self.actDelete = QAction('&Delete', self, shortcut='Del', statusTip="Delete selected items",
                                 triggered=self.onEditDelete)

        # self.actNew = self.createAction('&New','Ctrl+N','Create new graph',self.onFileNew)
        # self.actOpen = self.createAction('&Open', 'Ctrl+O', 'Open file',self.onFileOpen )
        # self.actSave = self.createAction('&Save', 'Ctrl+S', 'Save file',self.onFileSave )
        # self.actSaveAs = self.createAction('&Save &As...', 'Ctrl+Shift+s', 'Save file as...',
        #                                      self.onFileSaveAs )
        # self.actExit = self.createAction('&Exit', 'Ctrl+Q', 'Exit application',self.close )
        # self.actUndo = self.createAction('&Undo', 'Ctrl+Z', 'Undo last operation',
        #                                      self.onEditUndo)
        # self.actRedo = self.createAction('&Redo', 'Ctrl+Shift+Z', 'Redo last operation',
        #                                      self.onEditRedo)
        # self.actCut = self.createAction('Cu&t', 'Ctrl+X', 'Cut to clipboard',
        #                                      self.onEditCut)
        # self.actCopy = self.createAction('&Copy', 'Ctrl+C', 'Copy to clipboard',
        #                                      self.onEditCopy)
        # self.actPaste = self.createAction('&Paste', 'Ctrl+V', 'Copy to clipboard',
        #                                      self.onEditPaste)
        # self.Delete = self.createAction('&Delete', 'Del', 'Delete Selected items',
        #                                      self.onEditDelete)

    def initUI(self):

        self.createActions()
        # initialise Menu
        self.createMenus()
        self.node_editor = NodeEditorWidget(self)
        self.node_editor.scene.addHasBeenModifierdListeners(self.setTitle)
        self.setCentralWidget(self.node_editor)

        self.createStatusBar()

        # set Window properties
        # self.setWindowTitle("NodeEditor")
        self.setTitle()
        self.setGeometry(200, 200, 800, 500)

        self.show()

    def createStatusBar(self):
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        self.node_editor.view.scenePosChanged.connect(self.onScenePosChanged)

    def createMenus(self):
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&File')
        self.fileMenu.addAction(self.actNew)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actOpen)
        self.fileMenu.addAction(self.actSave)
        self.fileMenu.addAction(self.actSaveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actExit)

        self.editMenu = menubar.addMenu('&Edit')
        self.editMenu.addAction(self.actUndo)
        self.editMenu.addAction(self.actRedo)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actCut)
        self.editMenu.addAction(self.actCopy)
        self.editMenu.addAction(self.actPaste)

        self.editMenu.addSeparator()

        self.editMenu.addAction(self.actDelete)

    def setTitle(self):
        title ="Node Editor - "

        title +=  self.getCurrentNodeEditorWidget().getUserFriendlyFilename() # return scene
        # if self.node_editor.isFilenameSet() :
        #     title += "New"
        # else:
        #     title += os.path.basename(self.filename)
        # if self.centralWidget().scene.has_been_modified:
        # if self.centralWidget().isModified():
        # if self.getCurrentNodeEditorWidget().isModified():
        #     title += "*"

        self.setWindowTitle(title)




    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:event.ignore()

    def isModified(self):
        return self.getCurrentNodeEditorWidget().scene.has_been_modified

    def getCurrentNodeEditorWidget(self):
        return self.centralWidget()

    def maybeSave(self):
        if not self.isModified():
            return True
        res = QMessageBox.warning(self,"About to loose your work?",
                                  "The document has been modified.\n Do you want to save your changes?",
                                  QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        if res==QMessageBox.Save:
            return self.onFileSave()

        elif res == QMessageBox.Cancel:
            return False

        return True

    def onFileNew(self):
        if self.maybeSave():
            self.getCurrentNodeEditorWidget().scene.clear()
            self.filename = None
            self.setTitle()

    def onFileOpen(self):
        print('onFileOpen')
        if self.maybeSave():
            fname,filter = QFileDialog.getOpenFileName(self,'Open graph from file')
            if fname == '':
                return
            if os.path.isfile(fname):
                self.getCurrentNodeEditorWidget().scene.loadFromFile(fname)
                self.filename = fname
                self.setTitle()

    def onFileSave(self):
        print('onFileSave')
        if self.filename is None: return self.onFileSaveAs()
        self.getCurrentNodeEditorWidget().scene.saveToFile(self.filename)
        self.statusBar().showMessage("Successfully save file %s" % self.filename)
        return True


    def onFileSaveAs(self):
        print('onFileSaveAs')
        fname,filter=QFileDialog.getSaveFileName(self,'Save graph to file')
        if fname =='':
            return False
        self.filename = fname
        self.onFileSave()
        return True

    def onEditDelete(self):
        print('onEditDelete')
        self.getCurrentNodeEditorWidget().scene.grScene.views()[0].deleteSelected()

    def onEditUndo(self):
        print('onEditUndo')
        self.getCurrentNodeEditorWidget().scene.history.undo()

    def onEditRedo(self):
        print('onEditRedo')
        self.getCurrentNodeEditorWidget().scene.history.redo()



    def onEditPaste(self):
        row_data =  QApplication.clipboard().text()
        try:
            data = json.loads(row_data)
        except ValueError as e:
            print("pasting or not valid json data")
            return
        # check if data is correct
        if 'nodes' not in data:
            print("json does not contain any data!")
            return
        self.getCurrentNodeEditorWidget().scene.clipboard.deserializeFromClipboard(data)



    def onEditCut(self):
        print('onEditCut')
        data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(delete=True)
        str_data = json.dumps(data,indent=4)
        QApplication.clipboard().setText(str_data)

    def onEditCopy(self):
        data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(delete=False)
        print("data:",data)
        str_data = json.dumps(data, indent=4)
        print(str_data)
        QApplication.clipboard().setText(str_data)



    def close(self):
        print('close')

    def onScenePosChanged(self,x,y):
        self.status_mouse_pos.setText("Scene Pos[%d,%d]" %(x,y))

    def readSettings(self):
        settings = QSettings(self.name_company, self.name_product)
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QSettings(self.name_company, self.name_product)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

