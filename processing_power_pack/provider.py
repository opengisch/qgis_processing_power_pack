from qgis.core import QgsProcessingProvider

from .copy_file_algorithm import CopyFileAlgorithm
from .file_name_algorithm import FileNameAlgorithm
from .glob_files_algorithm import GlobFilesAlgorithm
from .make_folder_algorithm import MakeFolderAlgorithm
from .unzip_algorithm import UnzipAlgorithm
from .update_field_algorithm import UpdateFieldAlgorithm


class ProcessingPowerPackProvider(QgsProcessingProvider):
    def loadAlgorithms(self):
        self.addAlgorithm(UnzipAlgorithm())
        self.addAlgorithm(UpdateFieldAlgorithm())
        self.addAlgorithm(GlobFilesAlgorithm())
        self.addAlgorithm(CopyFileAlgorithm())
        self.addAlgorithm(MakeFolderAlgorithm())
        self.addAlgorithm(FileNameAlgorithm())

    def id(self):
        return "processingpowerpack"

    def name(self):
        return "Processing Power Pack"
