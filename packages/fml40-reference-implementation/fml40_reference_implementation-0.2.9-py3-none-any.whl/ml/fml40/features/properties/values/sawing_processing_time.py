from ml.ml40.features.properties.values.time import Time


class SawingProcessingTime(Time):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.remaining_time = None
        self.__json_out = dict()

    def to_json(self):
        self.__json_out = super().to_json()
        if self.remaining_time is not None:
            self.__json_out["remainingTime"] = self.remaining_time
        return self.__json_out
