from ml.ml40.features.properties.values.value import Value


class Velocity(Value):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.current_velocity = None
        self.max_velocity = None
        self.__json_out = dict()

    def to_json(self):
        self.__json_out = super().to_json()
        if self.current_velocity is not None:
            self.__json_out["currentVelocity"] = self.current_velocity
        if self.max_velocity is not None:
            self.__json_out["maxVelocity"] = self.max_velocity
        return self.__json_out