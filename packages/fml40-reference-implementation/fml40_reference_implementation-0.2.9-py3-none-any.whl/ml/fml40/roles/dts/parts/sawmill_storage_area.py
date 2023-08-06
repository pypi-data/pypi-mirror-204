from ml.ml40.roles.dts.parts.part import Part


class SawmillStorageArea(Part):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super(SawmillStorageArea, self).__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
