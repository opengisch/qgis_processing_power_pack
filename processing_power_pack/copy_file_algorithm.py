import os
import shutil

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
)


class CopyFileAlgorithm(QgsProcessingAlgorithm):
    INPUT_FILE = "INPUT_FILE"
    OUTPUT_FILE = "OUTPUT_FILE"
    OVERWRITE = "OVERWRITE"

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile(self.INPUT_FILE, "Input file"))
        self.addParameter(
            QgsProcessingParameterFileDestination(self.OUTPUT_FILE, "Destination file")
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.OVERWRITE, "Overwrite if exists", defaultValue=True
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        src = self.parameterAsFile(parameters, self.INPUT_FILE, context)
        dst = self.parameterAsFile(parameters, self.OUTPUT_FILE, context)
        overwrite = self.parameterAsBool(parameters, self.OVERWRITE, context)

        if not src or not os.path.isfile(src):
            raise QgsProcessingException("Input file not found: {}".format(src))

        if not dst:
            raise QgsProcessingException("No destination provided")

        dst_dir = os.path.dirname(os.path.abspath(dst))
        if dst_dir and not os.path.exists(dst_dir):
            try:
                os.makedirs(dst_dir)
            except Exception as e:
                raise QgsProcessingException(
                    "Could not create destination directory: {}".format(e)
                )

        if os.path.exists(dst) and not overwrite:
            raise QgsProcessingException(
                "Destination exists and overwrite is False: {}".format(dst)
            )

        try:
            shutil.copy2(src, dst)
        except Exception as e:
            raise QgsProcessingException("Failed to copy file: {}".format(e))

        return {self.OUTPUT_FILE: dst}

    def name(self):
        return "copyfile"

    def displayName(self):
        return "Copy File"

    def group(self):
        return "File Tools"

    def groupId(self):
        return "filetools"

    def createInstance(self):
        return CopyFileAlgorithm()

    def shortHelpString(self):
        return "Copies a file to the specified destination (optionally overwrite)."
