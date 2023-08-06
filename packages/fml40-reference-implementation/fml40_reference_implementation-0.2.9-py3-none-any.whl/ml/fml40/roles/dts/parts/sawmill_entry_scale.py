from ml.ml40.roles.dts.parts.scale import Scale


class SawmillEntryScale(Scale):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super(SawmillEntryScale, self).__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
