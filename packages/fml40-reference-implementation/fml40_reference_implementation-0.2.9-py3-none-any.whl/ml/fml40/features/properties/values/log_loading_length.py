from ml.ml40.features.properties.values.value import Value


class LogLoadingLength(Value):
    def __init__(self, namespace="fml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.min_length = None
        self.max_length = None
        self.__json_out = {}

    def to_json(self):
        self.__json_out = super().to_json()
        if self.min_length is not None:
            self.__json_out["minLength"] = self.min_length
        if self.max_length is not None:
            self.__json_out["maxLength"] = self.max_length
        return self.__json_out
