from qgis.core import QgsApplication

from .provider import ProcessingPowerPackProvider


def classFactory(iface):
    return ProcessingPowerPackPlugin(iface)


class ProcessingPowerPackPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.provider = ProcessingPowerPackProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
