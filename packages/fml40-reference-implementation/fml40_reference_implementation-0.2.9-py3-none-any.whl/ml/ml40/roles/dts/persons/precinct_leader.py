from ml.ml40.roles.dts.persons.person import Person


class PrecinctLeader(Person):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super(PrecinctLeader, self).__init__(namespace=namespace, name=name, identifier=identifier, parent=parent)