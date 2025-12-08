import os

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFolderDestination,
)


class MakeFolderAlgorithm(QgsProcessingAlgorithm):
    FOLDER = "FOLDER"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFolderDestination(self.FOLDER, "Folder to create")
        )

    def processAlgorithm(self, parameters, context, feedback):
        folder = self.parameterAsString(parameters, self.FOLDER, context)

        if not folder:
            raise QgsProcessingException("No folder path provided")

        try:
            if not os.path.exists(folder):
                os.makedirs(folder)
        except Exception as e:
            raise QgsProcessingException("Could not create folder: {}".format(e))

        return {self.FOLDER: folder}

    def name(self):
        return "makefolder"

    def displayName(self):
        return "Make Folder"

    def group(self):
        return "File Tools"

    def groupId(self):
        return "filetools"

    def createInstance(self):
        return MakeFolderAlgorithm()

    def shortHelpString(self):
        return "Creates the specified folder (no error if it already exists)."
