from ml.ml40.features.properties.values.value import Value


class Time(Value):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.time = None
        self.__json_out = dict()

    def to_json(self):
        self.__json_out = super().to_json()
        if self.time is not None:
            self.__json_out["time"] = self.time
        return self.__json_out
