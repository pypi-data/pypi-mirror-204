from ml.ml40.roles.dts.sensors.sensor import Sensor


class CounterSensor(Sensor):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super(CounterSensor, self).__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
