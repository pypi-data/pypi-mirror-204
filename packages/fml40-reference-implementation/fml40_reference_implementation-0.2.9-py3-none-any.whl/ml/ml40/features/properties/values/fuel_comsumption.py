from ml.ml40.features.properties.values.value import Value


class FuelConsumption(Value):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.currentConsumption = None
        self.meanConsumption = None
        self.__json_out = dict()

    def to_json(self):
        self.__json_out = super().to_json()
        if self.currentConsumption is not None:
            self.__json_out["currentConsumption"] = self.currentConsumption
        if self.meanConsumption is not None:
            self.__json_out["meanConsumption"] = self.meanConsumption
        return self.__json_out
