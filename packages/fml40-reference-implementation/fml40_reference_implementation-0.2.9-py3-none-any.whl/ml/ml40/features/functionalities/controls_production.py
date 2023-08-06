from ml.ml40.features.functionalities.functionality import Functionality


class ControlsProduction(Functionality):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace,
            name=name,
            identifier=identifier,
            parent=parent)

    def control(self):
        pass
