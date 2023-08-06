from ml.ml40.features.properties.values.value import Value


class StockVolume(Value):
    def __init__(self, namespace="fml40", name="", identifier="", parent=None):
        super().__init__(namespace=namespace, name=name, identifier=identifier, parent=parent)
        self.__stock = None
        self.__json_out = dict()

    @property
    def stock (self):
        return self.__stock 

    @stock .setter
    def stock (self, stock):
        self.__stock  = stock

    def to_json(self):
        self.__json_out = super().to_json()
        if self.stock  is not None:
            self.__json_out["stock"] = self.__stock 
        return self.__json_out

