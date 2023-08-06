from ml.ml40.features.properties.values.time import Time


class SawingSetupTime(Time):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
