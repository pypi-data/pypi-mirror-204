from ml.ml40.features.properties.values.time_slot import TimeSlot


class OpeningHours(TimeSlot):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )

