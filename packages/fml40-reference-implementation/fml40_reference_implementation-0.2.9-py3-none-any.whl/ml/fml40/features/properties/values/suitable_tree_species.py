from ml.fml40.features.properties.values.tree_species import TreeSpecies


class SuitableTreeSpecies(TreeSpecies):
    def __init__(self, namespace="fml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
