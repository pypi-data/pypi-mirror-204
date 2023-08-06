from ml.ml40.features.properties.values.value import Value


class Load(Value):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.load = None

    def to_json(self):
        self.__json_out = super().to_json()
        if self.load is not None:
            self.__json_out["load"] = self.load
        return self.__json_out
