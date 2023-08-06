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
import os

from PySide6 import QtCore

from cmlibs.argon.argondocument import ArgonDocument
from cmlibs.argon.argonlogger import ArgonLogger
from cmapps.neon.core.preferences import Preferences
from cmapps.neon.core.misc.neonerror import NeonError


class MainApplication(QtCore.QObject):

    documentChanged = QtCore.Signal()

    def __init__(self):
        super(MainApplication, self).__init__()
        self._saveUndoRedoIndex = 0
        self._currentUntoRedoIndex = 0

        self._location = None
        self._recents = []

        self._document = ArgonDocument()
        self._document.initialiseVisualisationContents()

        view_manager = self._document.getViewManager()
        view_manager.addViewByType("Layout1", "default")

        self._preferences = Preferences()

    def getZincContext(self):
        if self._document:
            return self._document.getZincContext()

        return None

    def isModified(self):
        return self._saveUndoRedoIndex != self._currentUntoRedoIndex

    def setCurrentUndoRedoIndex(self, index):
        self._currentUntoRedoIndex = index

    def setSaveUndoRedoIndex(self, index):
        self._saveUndoRedoIndex = index

    def setLocation(self, location):
        self._location = location

    def getLocation(self):
        return self._location

    def getViews(self):
        return self._document.getViewManager().getViews()

    def getActiveView(self):
        return self._document.getViewManager().getActiveView()

    def setActiveView(self, view):
        self._document.getViewManager().setActiveView(view)

    def new(self):
        """
        Create a blank document with the supplied project, or default project if not supplied
        """
        if self._document is not None:
            self._document.freeVisualisationContents()

        self._document = ArgonDocument()

        self._document.initialiseVisualisationContents()
        view_manager = self._document.getViewManager()
        view_manager.addViewByType("Layout1", "default")

        self.documentChanged.emit()

    def save(self):
        # make model sources relative to current location if possible
        # note that sources on different windows drives have absolute paths
        base_path = os.path.dirname(self._location)
        state = self._document.serialize(base_path)
        with open(self._location, 'w') as f:
            f.write(state)

    def load(self, filename):
        """
        Loads the named Neon file and on success sets filename as the current location.
        Emits documentChange separately if new document loaded, including if existing document cleared due to load failure.
        :return  True on success, otherwise False.
        """
        try:
            with open(filename, 'r') as f:
                state = f.read()
                self._location = None
                if self._document is not None:
                    self._document.freeVisualisationContents()
                self._document = ArgonDocument()
                self._document.initialiseVisualisationContents()
                # set current directory to path from file, to support scripts and fieldml with external resources
                path = os.path.dirname(filename)
                os.chdir(path)
                self._document.deserialize(state)
                self._location = filename
                self.documentChanged.emit()
                return True
        except (NeonError, IOError, ValueError) as e:
            ArgonLogger.getLogger().error("Failed to load Neon model " + filename + ": " + str(e))
        except:
            ArgonLogger.getLogger().error("Failed to load Neon model " + filename + ": Unknown error")

        return False

    def addRecent(self, recent):
        self.removeRecent(recent)
        self._recents.append(recent)

    def removeRecent(self, recent):
        if recent in self._recents:
            index = self._recents.index(recent)
            del self._recents[index]

    def getRecents(self):
        return self._recents

    def clearRecents(self):
        self._recents = []

    def getDocument(self):
        return self._document

    def getPreferences(self):
        return self._preferences
