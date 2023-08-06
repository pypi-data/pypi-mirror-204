from ml.ml40.roles.dts.organisations.organisation import Organisation


class ForwardingAgency(Organisation):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super(ForwardingAgency, self).__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
