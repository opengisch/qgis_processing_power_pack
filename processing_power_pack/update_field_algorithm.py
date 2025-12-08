from qgis.core import (
    QgsExpression,
    QgsExpressionContext,
    QgsExpressionContextUtils,
    QgsFeatureRequest,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterExpression,
    QgsProcessingParameterField,
    QgsProcessingParameterString,
    QgsProcessingParameterVectorLayer,
)


class UpdateFieldAlgorithm(QgsProcessingAlgorithm):
    LAYER = "LAYER"
    FIELD = "FIELD"
    EXPRESSION = "EXPRESSION"
    FILTER = "FILTER"

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer(self.LAYER, "Target layer"))
        self.addParameter(
            QgsProcessingParameterField(
                self.FIELD, "Field to update", parentLayerParameterName=self.LAYER
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.EXPRESSION, "Expression", parentLayerParameterName=self.LAYER
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.FILTER, "Filter (optional)", optional=True
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        layer = self.parameterAsVectorLayer(parameters, self.LAYER, context)
        field_name = self.parameterAsString(parameters, self.FIELD, context)
        expr_str = self.parameterAsString(parameters, self.EXPRESSION, context)
        filter_exp = self.parameterAsString(parameters, self.FILTER, context)

        if not layer:
            raise QgsProcessingException("Target layer not found")

        field_index = layer.fields().indexOf(field_name)
        if field_index == -1:
            raise QgsProcessingException("Field not found: {}".format(field_name))

        expr = QgsExpression(expr_str)
        if not expr or not expr.isValid():
            raise QgsProcessingException("Invalid expression: {}".format(expr_str))

        expr_ctx = QgsExpressionContext()
        expr_ctx.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

        if filter_exp:
            request = QgsFeatureRequest(QgsExpression(filter_exp))
        else:
            request = QgsFeatureRequest()

        if not layer.isEditable():
            layer.startEditing()

        for feat in layer.getFeatures(request):
            expr_ctx.setFeature(feat)
            value = expr.evaluate(expr_ctx)
            layer.changeAttributeValue(feat.id(), field_index, value)

        if not layer.commitChanges():
            raise QgsProcessingException("Failed to commit attribute changes")

        return {}

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading

    def name(self):
        return "updatefield"

    def displayName(self):
        return "Update Field"

    def group(self):
        return "Field Tools"

    def groupId(self):
        return "fieldtools"

    def createInstance(self):
        return UpdateFieldAlgorithm()

    def shortHelpString(self):
        return "Aktualisiert ein Feld mit dem Ergebnis einer Ausdrucksauswertung."
