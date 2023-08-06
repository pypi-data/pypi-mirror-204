from ml.ml40.features.properties.values.documents.contacts.contact import Contact


class OrganizationalContact(Contact):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.name = None
        self.__json_out = None

    def to_json(self):
        self.__json_out = super().to_json()
        if self.name is not None:
            self.__json_out["name"] = self.name
        return self.__json_out
