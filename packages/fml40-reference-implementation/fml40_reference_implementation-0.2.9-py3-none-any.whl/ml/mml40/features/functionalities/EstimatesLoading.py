from ml.ml40.features.functionalities.functionality import Functionality


class EstimatesLoading(Functionality):
    def __init__(self, namespace="mml40", name="", identifier="", parent=None):
        """Initializes the object.

        :param name: Object name
        :param identifier: Identifier

        """
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )

    def estimate(self):
        pass