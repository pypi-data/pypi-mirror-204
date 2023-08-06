from ml.ml40.features.properties.values.value import Value


class Measure(Value):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.data = None
        self.type = None
        self.description = None
        self.__json_out = dict()

    def to_json(self):
        self.__json_out = super().to_json()
        if self.data is not None:
            self.__json_out["data"] = self.data
        if self.type is not None:
            self.__json_out["type"] = self.type
        if self.description is not None:
            self.__json_out["description"] = self.description
        return self.__json_out
