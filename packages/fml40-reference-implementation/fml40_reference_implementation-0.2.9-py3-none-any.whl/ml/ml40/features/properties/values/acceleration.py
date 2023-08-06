from ml.ml40.features.properties.values.value import Value


class Acceleration(Value):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.x = None
        self.y = None
        self.z = None
        self.__json_out = dict()

    def to_json(self):
        self.__json_out = super().to_json()
        if self.x is not None:
            self.__json_out["x"] = self.x
        if self.y is not None:
            self.__json_out["y"] = self.y
        if self.z is not None:
            self.__json_out["z"] = self.z
        return self.__json_out