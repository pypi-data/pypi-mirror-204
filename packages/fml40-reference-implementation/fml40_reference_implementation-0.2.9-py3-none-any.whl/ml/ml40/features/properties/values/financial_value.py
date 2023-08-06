from ml.ml40.features.properties.values.value import Value


class FinancialValue(Value):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.__value = None
        self.__currency = None
        self.__json_out = dict()


    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, value):
        self.__currency = value


    def to_json(self):
        self.__json_out = super().to_json()
        if self.__value is not None:
            self.__json_out["value"] = self.__value

        if self.__currency is not None:
            self.__json_out["currency"] = self.__currency

        return self.__json_out
