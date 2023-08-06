"""
   Copyright 2015 University of Auckland

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import os.path

from PySide6 import QtCore, QtGui, QtWidgets

from cmapps.neon.ui.dialogs.aboutdialog import AboutDialog
from cmapps.neon.ui.ui_mainwindow import Ui_MainWindow
from cmapps.neon.undoredo.commands import CommandEmpty

from cmlibs.widgets.addviewwidget import AddView
from cmlibs.widgets.editabletabbar import EditableTabBar
from cmlibs.widgets.fieldlisteditorwidget import FieldListEditorWidget
from cmlibs.widgets.loggereditorwidget import LoggerEditorWidget
from cmlibs.widgets.materialeditorwidget import MaterialEditorWidget
from cmlibs.widgets.modelsourceseditorwidget import ModelSourcesEditorWidget, ModelSourcesModel
from cmlibs.widgets.regioneditorwidget import RegionEditorWidget
from cmlibs.widgets.sceneeditorwidget import SceneEditorWidget
from cmlibs.widgets.scenelayoutchooserdialog import SceneLayoutChooserDialog
from cmlibs.widgets.sceneviewereditorwidget import SceneviewerEditorWidget
from cmlibs.widgets.spectrumeditorwidget import SpectrumEditorWidget
from cmlibs.widgets.tessellationeditorwidget import TessellationEditorWidget
from cmlibs.widgets.timeeditorwidget import TimeEditorWidget
from cmlibs.widgets.viewwidget import ViewWidget


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, model):
        super(MainWindow, self).__init__()
        self._model = model

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._ui.viewTabWidget.setTabBar(EditableTabBar(self.parentWidget()))

        self._location = None  # The last location/directory used by the application
        self._current_view = None

        self._undoRedoStack = QtGui.QUndoStack(self)

        # Pre-create dialogs
        self._setupEditors()
        self._registerEditors()

        self._view_action_group = QtGui.QActionGroup(self)
        self._view_actions = []
        self._setup_views()
        self._setupOtherWindows()

        self._registerOtherWindows()

        self._addDockWidgets()

        self._makeConnections()

        # Set the undo redo stack state
        self._undoRedoStack.push(CommandEmpty())
        self._undoRedoStack.clear()

        self._updateUi()

        self._readSettings()

        self._onDocumentChanged()

    def _makeConnections(self):
        self._ui.action_Quit.triggered.connect(self.close)
        self._ui.action_New.triggered.connect(self._newTriggered)
        self._ui.action_Open.triggered.connect(self._openTriggered)
        self._ui.action_About.triggered.connect(self._aboutTriggered)
        self._ui.action_Save.triggered.connect(self._saveTriggered)
        self._ui.action_Save_As.triggered.connect(self._saveAsTriggered)
        self._ui.action_Snapshot.triggered.connect(self._snapshotTriggered)
        self._ui.action_Preferences.triggered.connect(self._preferencesTriggered)
        self._ui.action_Clear.triggered.connect(self._clearTriggered)
        self._ui.viewTabWidget.tabCloseRequested.connect(self._viewTabCloseRequested)
        self._ui.viewTabWidget.currentChanged.connect(self._currentViewChanged)
        tab_bar = self._ui.viewTabWidget.tabBar()
        tab_bar.tabTextEdited.connect(self._viewTabTextEdited)

        self._undoRedoStack.indexChanged.connect(self._undoRedoStackIndexChanged)
        self._undoRedoStack.canUndoChanged.connect(self._ui.action_Undo.setEnabled)
        self._undoRedoStack.canRedoChanged.connect(self._ui.action_Redo.setEnabled)

        self.dockWidgetContentsRegionEditor.regionSelected.connect(self._regionSelected)

        self._model.documentChanged.connect(self._onDocumentChanged)

    def _updateUi(self):
        modified = self._model.isModified()
        self._ui.action_Save.setEnabled(modified)
        recents = self._model.getRecents()
        self._ui.action_Clear.setEnabled(len(recents))

    def _addDockWidgets(self):
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidgetModelSourcesEditor)
        self.tabifyDockWidget(self.dockWidgetModelSourcesEditor, self.dockWidgetTessellationEditor)
        self.tabifyDockWidget(self.dockWidgetModelSourcesEditor, self.dockWidgetSpectrumEditor)
        self.tabifyDockWidget(self.dockWidgetModelSourcesEditor, self.dockWidgetMaterialEditor)
        self.tabifyDockWidget(self.dockWidgetModelSourcesEditor, self.dockWidgetSceneEditor)
        self.tabifyDockWidget(self.dockWidgetModelSourcesEditor, self.dockWidgetRegionEditor)
        self.tabifyDockWidget(self.dockWidgetModelSourcesEditor, self.dockWidgetSceneviewerEditor)
        self.tabifyDockWidget(self.dockWidgetModelSourcesEditor, self.dockWidgetFieldEditor)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dockWidgetLoggerEditor)
        self.tabifyDockWidget(self.dockWidgetLoggerEditor, self.dockWidgetTimeEditor)

    def _setupEditors(self):
        self.dockWidgetRegionEditor = QtWidgets.QDockWidget(self)
        self.dockWidgetRegionEditor.setWindowTitle('Region Editor')
        self.dockWidgetRegionEditor.setObjectName("dockWidgetRegionEditor")
        self.dockWidgetContentsRegionEditor = RegionEditorWidget()
        self.dockWidgetContentsRegionEditor.setObjectName("dockWidgetContentsRegionEditor")
        self.dockWidgetRegionEditor.setWidget(self.dockWidgetContentsRegionEditor)
        self.dockWidgetRegionEditor.setHidden(True)

        self.dockWidgetMaterialEditor = QtWidgets.QDockWidget(self)
        self.dockWidgetMaterialEditor.setWindowTitle('Material Editor')
        self.dockWidgetMaterialEditor.setObjectName("dockWidgetMaterialEditor")
        self.dockWidgetContentsMaterialEditor = MaterialEditorWidget()
        self.dockWidgetContentsMaterialEditor.setObjectName("dockWidgetContentsMaterialEditor")
        self.dockWidgetMaterialEditor.setWidget(self.dockWidgetContentsMaterialEditor)
        self.dockWidgetMaterialEditor.setHidden(True)

        self.dockWidgetModelSourcesEditor = QtWidgets.QDockWidget(self)
        self.dockWidgetModelSourcesEditor.setWindowTitle('Model Sources Editor')
        self.dockWidgetModelSourcesEditor.setObjectName("dockWidgetModelSourcesEditor")
        self.dockWidgetContentsModelSourcesEditor = ModelSourcesEditorWidget()
        self.dockWidgetContentsModelSourcesEditor.setObjectName("dockWidgetContentsModelSourcesEditor")
        self.dockWidgetModelSourcesEditor.setWidget(self.dockWidgetContentsModelSourcesEditor)
        self.dockWidgetModelSourcesEditor.setHidden(False)

        self.dockWidgetSceneEditor = QtWidgets.QDockWidget(self)
        self.dockWidgetSceneEditor.setWindowTitle('Scene Editor')
        self.dockWidgetSceneEditor.setObjectName("dockWidgetSceneEditor")
        self.dockWidgetContentsSceneEditor = SceneEditorWidget()
        self.dockWidgetContentsSceneEditor.setObjectName("dockWidgetContentsSceneEditor")
        self.dockWidgetSceneEditor.setWidget(self.dockWidgetContentsSceneEditor)
        self.dockWidgetSceneEditor.setHidden(True)

        self.dockWidgetSceneviewerEditor = QtWidgets.QDockWidget(self)
        self.dockWidgetSceneviewerEditor.setWindowTitle('Sceneviewer Editor')
        self.dockWidgetSceneviewerEditor.setObjectName("dockWidgetSceneviewerEditor")
        self.dockWidgetContentsSceneviewerEditor = SceneviewerEditorWidget(self.dockWidgetSceneviewerEditor)
        self.dockWidgetContentsSceneviewerEditor.setObjectName("dockWidgetContentsSceneviewerEditor")
        self.dockWidgetSceneviewerEditor.setWidget(self.dockWidgetContentsSceneviewerEditor)
        self.dockWidgetSceneviewerEditor.setHidden(True)
        self.dockWidgetSceneviewerEditor.visibilityChanged.connect(self.dockWidgetContentsSceneviewerEditor.setEnableUpdates)

        self.dockWidgetSpectrumEditor = QtWidgets.QDockWidget(self)
        self.dockWidgetSpectrumEditor.setWindowTitle('Spectrum Editor')
        self.dockWidgetSpectrumEditor.setObjectName("dockWidgetSpectrumEditor")
        self.dockWidgetContentsSpectrumEditor = SpectrumEditorWidget(self.dockWidgetSpectrumEditor)
        self.dockWidgetContentsSpectrumEditor.setObjectName("dockWidgetContentsSpectrumEditor")
        self.dockWidgetSpectrumEditor.setWidget(self.dockWidgetContentsSpectrumEditor)
        self.dockWidgetSpectrumEditor.setHidden(True)

        self.dockWidgetTessellationEditor = QtWidgets.QDockWidget(self)
        self.dockWidgetTessellationEditor.setWindowTitle('Tessellation Editor')
        self.dockWidgetTessellationEditor.setObjectName("dockWidgetTessellationEditor")
        self.dockWidgetContentsTessellationEditor = TessellationEditorWidget()
        self.dockWidgetContentsTessellationEditor.setObjectName("dockWidgetContentsTessellationEditor")
        self.dockWidgetTessellationEditor.setWidget(self.dockWidgetContentsTessellationEditor)
        self.dockWidgetTessellationEditor.setHidden(True)

        self.dockWidgetTimeEditor = QtWidgets.QDockWidget(self)
        self.dockWidgetTimeEditor.setWindowTitle('Time Editor')
        self.dockWidgetTimeEditor.setObjectName("dockWidgetTimeEditor")
        self.dockWidgetContentsTimeEditor = TimeEditorWidget()
        self.dockWidgetContentsTimeEditor.setObjectName("dockWidgetContentsTimeEditor")
        self.dockWidgetTimeEditor.setWidget(self.dockWidgetContentsTimeEditor)
        self.dockWidgetTimeEditor.setHidden(True)

        self.dockWidgetFieldEditor = QtWidgets.QDockWidget(self)
        self.dockWidgetFieldEditor.setWindowTitle('Field Editor')
        self.dockWidgetFieldEditor.setObjectName("dockWidgetFieldEditor")
        self.dockWidgetContentsFieldEditor = FieldListEditorWidget()
        self.dockWidgetContentsFieldEditor.setObjectName("dockWidgetContentsFieldEditor")
        self.dockWidgetFieldEditor.setWidget(self.dockWidgetContentsFieldEditor)
        self.dockWidgetFieldEditor.setHidden(True)

    def _registerEditors(self):
        self._registerEditor(self.dockWidgetRegionEditor)
        self._registerEditor(self.dockWidgetMaterialEditor)
        self._registerEditor(self.dockWidgetModelSourcesEditor)
        self._registerEditor(self.dockWidgetSceneEditor)
        self._registerEditor(self.dockWidgetSceneviewerEditor)
        self._registerEditor(self.dockWidgetSpectrumEditor)
        self._registerEditor(self.dockWidgetTessellationEditor)
        self._registerEditor(self.dockWidgetTimeEditor)
        self._registerEditor(self.dockWidgetFieldEditor)

        self._ui.menu_View.addSeparator()

    def _registerEditor(self, editor):
        menu = self._ui.menu_View

        toggle_action = editor.toggleViewAction()
        toggle_action.triggered.connect(self._view_dock_widget)
        menu.addAction(toggle_action)

    def _add_view_clicked(self):
        dlg = SceneLayoutChooserDialog(self)
        dlg.setModal(True)
        if dlg.exec_():
            layout = dlg.selected_layout()
            document = self._model.getDocument()
            view_manager = document.getViewManager()
            view_manager.addViewByType(layout)
            view_manager.setActiveView(layout)
            self._views_changed(view_manager)

    def _view_dock_widget(self, show):
        """
        If we are showing the dock widget we will make it current i.e. make sure it is visible if tabbed.
        """
        if show:
            sender_text = self.sender().text()
            for tab_bar in self.findChildren(QtWidgets.QTabBar):
                for index in range(tab_bar.count()):
                    tab_text = tab_bar.tabText(index)
                    if tab_text == sender_text:
                        tab_bar.setCurrentIndex(index)
                        return

    def _getEditorAction(self, action_name):
        action = None
        actions = self._ui.menu_View.actions()
        existing_actions = [a for a in actions if a.text() == action_name]
        if existing_actions:
            action = existing_actions[0]

        return action

    # def _createDialogs(self):
    #     self._snapshot_dialog = SnapshotDialog(self, self._ui.one_gl_widget_to_rule_them_all)
    #     self._snapshot_dialog.setZincContext(self._model.getZincContext())

    #     self._preferences_dialog = PreferencesDialog(self)

    def _writeSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        settings.setValue('location', self._location)
        settings.setValue('geometry', self.saveGeometry())

        settings.beginWriteArray('recents')
        recents = self._model.getRecents()
        for i, r in enumerate(recents):
            settings.setArrayIndex(i)
            settings.setValue('item', r)
        settings.endArray()
        settings.endGroup()

        settings.beginGroup('SnapshotDialog')
        # settings.setValue('state', self._snapshot_dialog.serialize())
        settings.endGroup()

    def _readSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        geometry = settings.value('geometry')
        if geometry is not None:
            self.restoreGeometry(geometry)
        self._location = settings.value('location', QtCore.QDir.homePath())

        size = settings.beginReadArray('recents')
        for i in range(size):
            settings.setArrayIndex(i)
            self._addRecent(settings.value('item'))
        settings.endArray()
        settings.endGroup()

        settings.beginGroup('SnapshotDialog')
        # self._snapshot_dialog.deserialize(settings.value('state', ''))
        settings.endGroup()

        self._updateUi()

    def _addRecent(self, recent):
        actions = self._ui.menu_Open_Recent.actions()
        insert_before_action = actions[0]
        self._model.addRecent(recent)
        recent_action = QtGui.QAction(self._ui.menu_Open_Recent)
        recent_action.setText(recent)
        self._ui.menu_Open_Recent.insertAction(insert_before_action, recent_action)
        recent_action.triggered.connect(self._open)

    def _setCurrentView(self, index):
        v = self._ui.viewTabWidget.widget(int(index))
        self._changeView(v)
        self._postChangeView()

    def _storeCurrentView(self):
        pass

    def _preChangeView(self):
        pass

    def _changeView(self, view):
        self._ui.viewTabWidget.setCurrentWidget(view)

    def _postChangeView(self):
        pass

    def _setupOtherWindows(self):
        self.dockWidgetLoggerEditor = QtWidgets.QDockWidget("Log Viewer", self)
        # self.dockWidgetLoggerEditor.setWindowTitle('Logger')
        self.dockWidgetLoggerEditor.setObjectName("dockWidgetLoggerEditor")
        logger_widget = LoggerEditorWidget(self.dockWidgetLoggerEditor)
        # logger_widget.setObjectName("dockWidgetContentsLoggerEditor")
        self.dockWidgetLoggerEditor.setWidget(logger_widget)
        self.dockWidgetLoggerEditor.setHidden(True)

    def _registerOtherWindows(self):
        self._registerOtherWindow(self.dockWidgetLoggerEditor)

    def _registerOtherWindow(self, editor):
        action = self._getEditorAction("Other Windows")
        if action is None:
            menu = self._ui.menu_View.addMenu("Other Windows")
            menu.setEnabled(True)
        else:
            menu = action.menu()

        toggle_action = editor.toggleViewAction()
        toggle_action.triggered.connect(self._view_dock_widget)
        menu.addAction(toggle_action)

    def _viewTabCloseRequested(self, index):
        document = self._model.getDocument()
        view_manager = document.getViewManager()
        view_manager.removeView(index)
        self._views_changed(view_manager)

    def _viewTabTextEdited(self, index, value):
        document = self._model.getDocument()
        view_manager = document.getViewManager()
        view = view_manager.getView(index)
        view.setName(value)

    def _currentViewChanged(self, index):
        document = self._model.getDocument()
        view_manager = document.getViewManager()
        view_manager.setActiveView(self._ui.viewTabWidget.tabText(index))

    def _setup_views(self):
        icon = QtGui.QIcon(":/widgets/images/icons/list-add-icon.png")
        btn = QtWidgets.QToolButton()
        btn.setStyleSheet("border-radius: 0.75em; border-width: 1px; border-style: solid; border-color: dark-grey;"
                          " background-color: grey; min-width: 1.5em; min-height: 1.5em; margin-right: 1em;")
        btn.setIcon(icon)
        btn.setAutoFillBackground(True)
        btn.clicked.connect(self._add_view_clicked)

        self._ui.viewTabWidget.setCornerWidget(btn)

    def _current_sceneviewer_changed(self):
        sceneviewer = self._ui.viewTabWidget.currentWidget().getActiveSceneviewer()
        self.dockWidgetContentsSceneviewerEditor.setSceneviewer(sceneviewer)

    def _views_changed(self, view_manager):
        views = view_manager.getViews()
        active_view = view_manager.getActiveView()

        # Remove existing views from menu
        for view_action in self._view_actions:
            self._view_action_group.removeAction(view_action)
            self._ui.menu_View.removeAction(view_action)

        self._view_actions = []

        # Remove all views.
        self._ui.viewTabWidget.clear()
        tab_bar = self._ui.viewTabWidget.tabBar()

        if views:
            tab_bar.set_editable(True)
            active_widget = None
            separator_action = self._ui.menu_View.addSeparator()
            separator_action.setActionGroup(self._view_action_group)
            self._view_actions.append(separator_action)
            # Instate views.
            for v in views:
                w = ViewWidget(v.getScenes(), v.getGridSpecification(), self._ui.viewTabWidget)
                # w.graphicsReady.connect(self._view_graphics_ready)
                w.currentChanged.connect(self._current_sceneviewer_changed)
                w.setContext(view_manager.getZincContext())
                view_name = v.getName()
                self._ui.viewTabWidget.addTab(w, view_name)

                if active_view == view_name:
                    active_widget = w

                action_view = QtGui.QAction(view_name, self)
                action_view.setData(w)
                # action_view.setCheckable(True)
                action_view.setActionGroup(self._view_action_group)
                action_view.triggered.connect(self._viewTriggered)
                action_view.setCheckable(True)
                self._ui.menu_View.addAction(action_view)
                self._view_actions.append(action_view)

            if active_widget is not None:
                self._ui.viewTabWidget.setCurrentWidget(w)
            else:
                self._ui.viewTabWidget.setCurrentIndex(0)
            self._ui.viewTabWidget.setTabsClosable(True)
        else:
            tab_bar.set_editable(False)

            add_view = AddView()
            add_view.clicked.connect(self._add_view_clicked)
            self._ui.viewTabWidget.addTab(add_view, "Add View")
            self._ui.viewTabWidget.setTabsClosable(False)

    def _viewTriggered(self):
        v = self.sender().data()
        self._preChangeView()
        self._changeView(v)
        self._postChangeView()

    def _onDocumentChanged(self):
        document = self._model.getDocument()
        rootRegion = document.getRootRegion()
        zincRootRegion = rootRegion.getZincRegion()

        # need to pass new Zinc context to dialogs and widgets using global modules
        zincContext = document.getZincContext()
        self.dockWidgetContentsSpectrumEditor.setSpectrums(document.getSpectrums())
        self.dockWidgetContentsMaterialEditor.setMaterials(document.getMaterials())
        self.dockWidgetContentsTessellationEditor.setTessellations(document.getTessellations())
        self.dockWidgetContentsTimeEditor.setZincContext(zincContext)
        # self._snapshot_dialog.setZincContext(zincContext)

        model_sources_model = ModelSourcesModel(document, [])
        self.dockWidgetContentsModelSourcesEditor.setModelSourcesModel(zincRootRegion, model_sources_model)

        # need to pass new root region to the following
        self.dockWidgetContentsRegionEditor.setRootRegion(rootRegion)
        self.dockWidgetContentsSceneEditor.setZincRootRegion(zincRootRegion)
        self.dockWidgetContentsSceneviewerEditor.setZincRootRegion(zincRootRegion)
        self.dockWidgetContentsFieldEditor.setRootArgonRegion(rootRegion)
        self.dockWidgetContentsFieldEditor.setTimekeeper(zincContext.getTimekeepermodule().getDefaultTimekeeper())

        view_manager = document.getViewManager()
        self._views_changed(view_manager)

    def _regionSelected(self, region):
        # self.dockWidgetContentsModelSourcesEditor.setRegion(region)
        zincRegion = region.getZincRegion()
        # scene = zincRegion.getScene()
        # self.dockWidgetContentsSceneEditor.setScene(scene)
        # self.dockWidgetContentsFieldEditor.setFieldmodule(zincRegion.getFieldmodule())
        # self.dockWidgetContentsFieldEditor.setArgonRegion(region)

    def _visualisationViewReady(self):
        self._visualisation_view_ready = True
        if self._visualisation_view_state_update_pending:
            self._restoreSceneviewerState()

    def _saveTriggered(self):
        if self._model.getLocation() is None:
            self._saveAsTriggered()
        else:
            self._recordSceneviewerState()
            self._model.save()

    def _saveAsTriggered(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, caption='Choose file ...', dir=self._location, filter="Neon Files (*.neon *.json);;All (*.*)")
        if filename:
            self._location = os.path.dirname(filename)
            self._model.setLocation(filename)
            self._recordSceneviewerState()
            self._model.save()

    def _restoreSceneviewerState(self):
        document = self._model.getDocument()
        sceneviewer_state = document.getSceneviewer().serialize()
        # self._visualisation_view.setSceneviewerState(sceneviewer_state)
        # self.dockWidgetContentsSceneviewerEditor.setSceneviewer(self._visualisation_view.getSceneviewer())
        self._visualisation_view_state_update_pending = False

    def _recordSceneviewerState(self):
        document = self._model.getDocument()
        view_manager = document.getViewManager()
        for index in range(self._ui.viewTabWidget.count()):
            tab = self._ui.viewTabWidget.widget(index)
            tab_layout = tab.layout()

            view = view_manager.getView(index)
            view.setName(self._ui.viewTabWidget.tabText(index))

            rows = tab_layout.rowCount()
            columns = tab_layout.columnCount()
            for r in range(rows):
                for c in range(columns):
                    sceneviewer_widget = tab_layout.itemAtPosition(r, c).widget()
                    view.updateSceneviewer(r, c, sceneviewer_widget.getSceneviewer())

    def _undoRedoStackIndexChanged(self, index):
        self._model.setCurrentUndoRedoIndex(index)

    def _aboutTriggered(self):
        d = AboutDialog(self)
        d.exec_()

    def _snapshotDialogReady(self):
        document = self._model.getDocument()
        rootRegion = document.getRootRegion()
        zincRootRegion = rootRegion.getZincRegion()
        scene = zincRootRegion.getScene()
        self._snapshot_dialog.setScene(scene)

    def _snapshotTriggered(self):
        if self._snapshot_dialog.getLocation() is None and self._location is not None:
            self._snapshot_dialog.setLocation(self._location)

        if self._snapshot_dialog.exec_():
            if self._location is None:
                self._location = self._snapshot_dialog.getLocation()
            filename = self._snapshot_dialog.getFilename()
            wysiwyg = self._snapshot_dialog.getWYSIWYG()
            width = self._snapshot_dialog.getWidth()
            height = self._snapshot_dialog.getHeight()
            self._visualisation_view.saveImage(filename, wysiwyg, width, height)

    def _preferencesTriggered(self):
        if self._preferences_dialog.exec_():
            pass  # Save the state

    def _newTriggered(self):
        self._model.new()

    def _openModel(self, filename):
        success = self._model.load(filename)
        if success:
            self._location = os.path.dirname(filename)
            self._addRecent(filename)
        else:
            QtWidgets.QMessageBox.warning(self, "Load failure", "Failed to load file " + filename + ". Refer to logger window for more details", QtWidgets.QMessageBox.Ok)
            self._model.new()  # in case document half constructed; emits documentChanged

        self._updateUi()

    def _openTriggered(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, caption='Choose file ...', dir=self._location, filter="Neon Files (*.neon *.json);;All (*.*)")

        if filename:
            self._openModel(filename)

    def _open(self):
        """
        Open a model from a recent file.
        """
        filename = self.sender().text()
        self._ui.menu_Open_Recent.removeAction(self.sender())
        self._model.removeRecent(filename)
        self._openModel(filename)

    def _clearTriggered(self):
        self._model.clearRecents()
        actions = self._ui.menu_Open_Recent.actions()
        for action in actions[:-2]:
            self._ui.menu_Open_Recent.removeAction(action)

        self._updateUi()

    def confirmClose(self):
        # Check to see if the Workflow is in a saved state.
        if self._model.isModified():
            ret = QtWidgets.QMessageBox.warning(self, 'Unsaved Changes', 'You have unsaved changes, would you like to save these changes now?',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if ret == QtWidgets.QMessageBox.Yes:
                self._saveTriggered()

    def _quitApplication(self):
        self.confirmClose()
        self._writeSettings()

    def closeEvent(self, event):
        self._quitApplication()
        super(MainWindow, self).closeEvent(event)
