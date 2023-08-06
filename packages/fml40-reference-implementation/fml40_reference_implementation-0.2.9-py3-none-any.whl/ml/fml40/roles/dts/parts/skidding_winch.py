from ml.ml40.roles.dts.parts.winch import Winch


class SkiddingWinch(Winch):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super(SkiddingWinch, self).__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
