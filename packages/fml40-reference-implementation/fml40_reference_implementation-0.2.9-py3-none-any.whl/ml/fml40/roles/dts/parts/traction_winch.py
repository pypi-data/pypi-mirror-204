from ml.ml40.roles.dts.parts.winch import Winch


class TractionWinch(Winch):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super(TractionWinch, self).__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
