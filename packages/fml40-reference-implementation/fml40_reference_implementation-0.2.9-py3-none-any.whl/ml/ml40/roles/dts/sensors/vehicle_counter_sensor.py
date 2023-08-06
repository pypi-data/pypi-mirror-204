from ml.ml40.roles.dts.sensors.counter_sensor import CounterSensor


class VehicleCounterSensor(CounterSensor):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super(VehicleCounterSensor, self).__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
