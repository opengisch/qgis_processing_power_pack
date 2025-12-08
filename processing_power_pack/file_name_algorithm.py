import os

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingOutputString,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFile,
)


class FileNameAlgorithm(QgsProcessingAlgorithm):
    INPUT_PATH = "INPUT_PATH"
    OPERATION = "OPERATION"
    RESULT = "RESULT"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_PATH,
                "Input path (file or folder)",
                behavior=QgsProcessingParameterFile.File,
            )
        )
        ops = ["parent", "basename", "name", "extension"]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.OPERATION, "Operation", options=ops, defaultValue=0
            )
        )
        self.addOutput(QgsProcessingOutputString(self.RESULT, "Result"))

    def processAlgorithm(self, parameters, context, feedback):
        path = self.parameterAsFile(parameters, self.INPUT_PATH, context)
        op = self.parameterAsEnum(parameters, self.OPERATION, context)

        if not path:
            raise QgsProcessingException("No input path provided")

        abs_path = os.path.abspath(path)

        if op == 0:  # parent
            result = os.path.dirname(abs_path)
        elif op == 1:  # basename
            result = os.path.basename(abs_path)
        elif op == 2:  # name without extension
            result = os.path.splitext(os.path.basename(abs_path))[0]
        elif op == 3:  # extension without dot
            ext = os.path.splitext(os.path.basename(abs_path))[1]
            result = ext[1:] if ext.startswith(".") else ext
        else:
            raise QgsProcessingException("Unknown operation")

        return {self.RESULT: result}

    def name(self):
        return "filepathops"

    def displayName(self):
        return "File Path Operations"

    def group(self):
        return "File Tools"

    def groupId(self):
        return "filetools"

    def createInstance(self):
        return FileNameAlgorithm()

    def helpString(self):
        return (
            "File Path Operations\n\n"
            "Available operations (choose one):\n"
            "- parent: Returns the parent directory of the given path.\n"
            "  Example: '/home/user/data/file.shp' -> '/home/user/data'\n"
            "           'C:\\\\temp\\\\report.pdf' -> 'C:\\\\temp'\n\n"
            "- basename: Returns the file name including extension.\n"
            "  Example: '/home/user/data/file.shp' -> 'file.shp'\n\n"
            "- name: Returns the file name without its extension.\n"
            "  Example: '/home/user/data/file.shp' -> 'file'\n\n"
            "- extension: Returns the file extension without the leading dot.\n"
            "  Example: '/home/user/data/file.shp' -> 'shp'\n\n"
            "Notes:\n"
            "- The input may be a file or folder path. For folder paths, basename/name/extension behave accordingly.\n"
            "- Paths are normalized to absolute paths before evaluation.\n"
            "- Use this tool to extract a single string result; use batch processing to handle many paths.\n"
        )

    def shortHelpString(self):
        return (
            "Return various parts of a file path (parent, basename, name, extension)."
        )
