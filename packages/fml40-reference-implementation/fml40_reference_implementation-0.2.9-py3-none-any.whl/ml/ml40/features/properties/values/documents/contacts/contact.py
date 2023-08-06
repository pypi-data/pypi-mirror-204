from ml.ml40.features.properties.values.documents.document import Document


class Contact(Document):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.name = None
        self.address = None
        self.telefon = None
        self.mobil = None
        self.fax = None
        self.email = None
        self.__json_out = None

    def to_json(self):
        self.__json_out = super().to_json()
        if self.address is not None:
            self.__json_out["address"] = self.address
        if self.telefon is not None:
            self.__json_out["telefon"] = self.telefon
        if self.mobil is not None:
            self.__json_out["mobil"] = self.mobil
        if self.fax is not None:
            self.__json_out["fax"] = self.fax
        if self.email is not None:
            self.__json_out["eMail"] = self.email
        return self.__json_out
