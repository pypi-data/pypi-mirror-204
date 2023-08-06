from ml.ml40.features.properties.values.value import Value


class GroundClearance(Value):
    def __init__(self, namespace="fml40", name="", identifier="", parent=None):
        super().__init__(namespace=namespace, name=name, identifier=identifier, parent=parent)

        self.ground_type = None
        self.height = None

    def to_json(self):
        self.__json_out = super().to_json()
        if self.ground_type is not None:
            self.__json_out["groundType"] = self.ground_type
        if self.height is not None:
            self.__json_out["height"] = self.height
        return self.__json_out
