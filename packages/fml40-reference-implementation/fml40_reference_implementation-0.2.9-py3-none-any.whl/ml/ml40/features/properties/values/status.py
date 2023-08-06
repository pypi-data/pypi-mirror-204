from ml.ml40.features.properties.values.value import Value


class Status(Value):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.status = None
        self.__json_out = dict()

    def to_json(self):
        self.__json_out = super().to_json()
        if self.status is not None:
            self.__json_out["status"] = self.status
        return self.__json_out
