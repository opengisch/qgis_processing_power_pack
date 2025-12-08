import os
import zipfile

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFile,
    QgsProcessingParameterFolderDestination,
)


class UnzipAlgorithm(QgsProcessingAlgorithm):
    INPUT_ZIP = "INPUT_ZIP"
    OUTPUT_FOLDER = "OUTPUT_FOLDER"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(self.INPUT_ZIP, "Zip file", extension="zip")
        )
        self.addParameter(
            QgsProcessingParameterFolderDestination(self.OUTPUT_FOLDER, "Output folder")
        )

    def processAlgorithm(self, parameters, context, feedback):
        zip_path = self.parameterAsFile(parameters, self.INPUT_ZIP, context)
        out_folder = self.parameterAsString(parameters, self.OUTPUT_FOLDER, context)

        if not zip_path or not os.path.isfile(zip_path):
            raise QgsProcessingException("Zip file not found: {}".format(zip_path))

        if not os.path.exists(out_folder):
            try:
                os.makedirs(out_folder)
            except OSError as e:
                raise QgsProcessingException(
                    "Could not create output folder: {}".format(e)
                )

        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(out_folder)
        except zipfile.BadZipFile:
            raise QgsProcessingException("Bad zip file: {}".format(zip_path))
        except Exception as e:
            feedback.reportError("Error while extracting zip: {}".format(e))
            raise QgsProcessingException(str(e))

        return {self.OUTPUT_FOLDER: out_folder}

    def name(self):
        return "unzipfile"

    def displayName(self):
        return "Unzip File"

    def group(self):
        return "File Tools"

    def groupId(self):
        return "filetools"

    def createInstance(self):
        return UnzipAlgorithm()

    def shortHelpString(self):
        return "Entpackt eine ZIP-Datei in den angegebenen Ausgabeordner."
