from ml.ml40.features.properties.values.documents.contacts.contact import Contact


class PersonalContact(Contact):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.first_name = None
        self.last_name = None
        self.address = None
        self.telefon = None
        self.mobil = None
        self.fax = None
        self.email = None
        self.company = None
        self.__json_out = dict()

    def to_json(self):
        self.__json_out = super().to_json()
        if self.first_name is not None:
            self.__json_out["firstName"] = self.first_name
        if self.last_name is not None:
            self.__json_out["lastName"] = self.last_name
            self.__json_out["company"] = self.company
        return self.__json_out