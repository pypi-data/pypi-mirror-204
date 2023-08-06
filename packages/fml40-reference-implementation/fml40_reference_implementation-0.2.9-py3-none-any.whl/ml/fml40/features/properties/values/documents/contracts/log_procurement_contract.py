from ml.ml40.features.properties.values.documents.contracts.contract import Contract


class LogProcurementContract(Contract):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
