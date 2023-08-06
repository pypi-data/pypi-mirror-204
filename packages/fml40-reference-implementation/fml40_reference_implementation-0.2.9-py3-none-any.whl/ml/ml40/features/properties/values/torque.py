from ml.ml40.features.properties.values.value import Value


class Torque(Value):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(namespace=namespace, name=name, identifier=identifier, parent=parent)
        self.max_torque = None
        self.current_torque = None
        self.__json_out = dict()

    def to_json(self):
        self.__json_out = super().to_json()
        if self.max_torque  is not None:
            self.__json_out["maxTorque"] = self.max_torque
        if self.current_torque  is not None:
            self.__json_out["currentTorque"] = self.current_torque
        return self.__json_out