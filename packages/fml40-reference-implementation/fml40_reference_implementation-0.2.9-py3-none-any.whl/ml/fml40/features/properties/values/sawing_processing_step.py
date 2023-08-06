from ml.ml40.features.properties.values.value import Value


class SawingProcessingStep(Value):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.current_step = None
        self.__json_out = dict()

    def to_json(self):
        self.__json_out = super().to_json()
        if self.current_step is not None:
            self.__json_out["currentStep"] = self.current_step
        return self.__json_out
