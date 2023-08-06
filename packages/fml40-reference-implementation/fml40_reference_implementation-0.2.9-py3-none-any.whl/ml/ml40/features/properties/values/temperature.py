from ml.ml40.features.properties.values.value import Value


class Temperature(Value):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.temperature = None
        self.__json_out = dict()

    def to_json(self):
        self.__json_out = super().to_json()
        if self.temperature is not None:
            self.__json_out["temperature"] = self.temperature
        return self.__json_out
