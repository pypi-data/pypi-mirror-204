from ml.ml40.features.functionalities.controls_production import ControlsProduction


class ControlsSawmillProduction(ControlsProduction):
    def __init__(self, namespace="fml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )

    def control(self):
        pass
