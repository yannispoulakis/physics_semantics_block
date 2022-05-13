from owlready2 import default_world


class service_onto_rules:
    def __init__(self, onto):
        self.onto = onto
        self.find_cluster = """
        PREFIX vocab:      <http://www.physics-h2020.eu/physics/resources_ontology#>

        SELECT ?s 
        WHERE {?s a vocab:Cluster .}"""
        pass

    def add_locality(self):
        # sparql , second parameter skips error for undefined individuals.
        # If no cluster individuals are found this step is skipped.
        qres = default_world.sparql(self.find_cluster, error_on_undefined_entities=False)
        qres = list(qres)
        if len(qres) == 0:
            print("No locality added, cluster individuals not found!")

        for row in qres:
            cluster = row[0]

            if all(node.ClusterNodeIsHostedOn[0].is_a[0] == self.onto.SingleBoardUnit for node in
                   cluster.ConsistsOfNodes):
                cluster.hasLocality = "edge"

            elif any(node.ClusterNodeIsHostedOn[0].is_a[0] == self.onto.SingleBoardUnit for node in
                     cluster.ConsistsOfNodes):
                cluster.hasLocality = "hybrid"

            else:
                cluster.hasLocality = "cloud"

