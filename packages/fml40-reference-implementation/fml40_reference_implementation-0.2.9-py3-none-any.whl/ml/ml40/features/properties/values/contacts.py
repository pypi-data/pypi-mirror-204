from ml.ml40.features.properties.values.value import Value


class Contacts(Value):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.__json_out = dict()


