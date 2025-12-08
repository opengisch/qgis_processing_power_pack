import glob
import os

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingOutputString,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFile,
    QgsProcessingParameterString,
)


class GlobFilesAlgorithm(QgsProcessingAlgorithm):
    INPUT_FOLDER = "INPUT_FOLDER"
    PATTERN = "PATTERN"
    RECURSIVE = "RECURSIVE"
    MATCHES = "MATCHES"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_FOLDER,
                "Input folder",
                behavior=QgsProcessingParameterFile.Folder,
            )
        )
        self.addParameter(
            QgsProcessingParameterString(self.PATTERN, "Glob pattern (e.g. *.shp)")
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.RECURSIVE, "Recursive", defaultValue=False
            )
        )
        self.addOutput(
            QgsProcessingOutputString(
                self.MATCHES, "Matches (list of paths as strings)"
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        folder = self.parameterAsString(parameters, self.INPUT_FOLDER, context)
        pattern = self.parameterAsString(parameters, self.PATTERN, context)
        recursive = self.parameterAsBool(parameters, self.RECURSIVE, context)

        if not folder or not os.path.isdir(folder):
            raise QgsProcessingException("Input folder not found: {}".format(folder))

        if not pattern:
            raise QgsProcessingException("Pattern is empty")

        search = (
            os.path.join(folder, "**", pattern)
            if recursive
            else os.path.join(folder, pattern)
        )
        files = [os.path.abspath(p) for p in glob.glob(search, recursive=recursive)]

        return {self.MATCHES: "\n".join(files)}

    def name(self):
        return "globfiles"

    def displayName(self):
        return "Glob Files"

    def group(self):
        return "File Tools"

    def groupId(self):
        return "filetools"

    def createInstance(self):
        return GlobFilesAlgorithm()

    def shortHelpString(self):
        return "Searches a directory for files matching a glob pattern and returns the paths as string(s)."
