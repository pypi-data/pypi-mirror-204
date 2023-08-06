from ml.ml40.features.properties.values.value import Value


class BankAccount(Value):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.IBAN = None
        self.BIC = None
        self.AccountOwner = None
        self.__json_out = dict()

    def BankAccount(self):
        self.__json_out = super().to_json()
        if self.IBAN is not None:
            self.__json_out["IBAN"] = self.IBAN#
        if self.BIC is not None:
            self.__json_out["BIC"] = self.BIC
        if self.AccountOwner is not None:
            self.__json_out["AccountOwner"] = self.AccountOwner
        return self.__json_out
