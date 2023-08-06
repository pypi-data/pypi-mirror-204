from ml.ml40.features.properties.values.load import Load

class LoadIndex(Load):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.index = None

    def to_json(self):
        self.__json_out = super().to_json()
        if self.index is not None:
            self.__json_out["index"] = self.index
        return self.__json_out
