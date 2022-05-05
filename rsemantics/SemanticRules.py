from owlready2 import default_world


class service_onto_rules:
    def __init__(self, onto):
        self.onto = onto
        self.find_cluster = """
        PREFIX vocab:      <http://www.physics-h2020.eu/physics/>

        SELECT ?s 
        WHERE {?s a vocab:Cluster .}"""
        pass

    def add_locality(self):
        qres = default_world.sparql(self.find_cluster)
        for row in qres:
            print(row)
            cluster = row[0]
            print(cluster.ConsistsOfNodes[0].ClusterNodeIsHostedOn[0].is_a[0])
            if all(node.ClusterNodeIsHostedOn[0].is_a[0] == self.onto.SingleBoardUnit for node in cluster.ConsistsOfNodes):
                cluster.hasLocality = "edge"
            elif any(node.ClusterNodeIsHostedOn[0].is_a[0] == self.onto.SingleBoardUnit for node in cluster.ConsistsOfNodes):
                cluster.hasLocality = "hybrid"
            else:
                cluster.hasLocality = "cloud"

