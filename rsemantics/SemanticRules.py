import ontospy.cli
from owlready2 import default_world


class service_onto_rules:
    def __init__(self):
        self.find_cluster = """
        PREFIX vocab:      <http://www.physics-h2020.eu/physics/>

        SELECT ?s 
        WHERE {?s a vocab:Cluster .}"""
        pass

    def add_locality(self):
        qres = default_world.sparql(knows_query)
        for row in qres:
            print(row)
            cluster = row[0]
            print(cluster.ConsistsOfNodes[0].ClusterNodeIsHostedOn[0].is_a[0])
            if all(node.ClusterNodeIsHostedOn[0].is_a[0] == onto.SingleBoardUnit for node in cluster.ConsistsOfNodes):
                cluster.hasLocality = "edge"
            elif any(node.ClusterNodeIsHostedOn[0].is_a[0] == onto.SingleBoardUnit for node in cluster.ConsistsOfNodes):
                cluster.hasLocality = "hybrid"
            else:
                cluster.hasLocality = "cloud"


knows_query = """
       PREFIX vocab:      <http://www.physics-h2020.eu/physics/>

       SELECT ?s 
       WHERE {?s a vocab:Cluster .}"""

qres = default_world.sparql(knows_query)

for row in qres:
    print(row)
    cluster = row[0]
    print(cluster.ConsistsOfNodes[0].ClusterNodeIsHostedOn[0].is_a[0])
    if all(node.ClusterNodeIsHostedOn[0].is_a[0] == onto.SingleBoardUnit for node in cluster.ConsistsOfNodes):
        cluster.hasLocality = "edge"
    elif any(node.ClusterNodeIsHostedOn[0].is_a[0] == onto.SingleBoardUnit for node in cluster.ConsistsOfNodes):
        cluster.hasLocality = "hybrid"
    else:
        cluster.hasLocality = "cloud"

knows_query2 = """
       PREFIX vocab:      <http://www.physics-h2020.eu/physics/>

       SELECT *
       WHERE {?s  vocab:ClusterNodeIsHostedOn ?e .}"""

qres = default_world.sparql(knows_query2)

for item in qres:
    print(item[0], item[0].OperatesWith)
    print(item[1], item[1].OperatesWith)

    if item[1].is_a[0] == onto.SingleBoardUnit:
        item[0].hasRamCapacity = getattr(item[1].hasRawComputationalUnit[0], "withNumValue")
        item[0].hasCPUCapacity = getattr(item[1].hasRawComputationalUnit[1], "withNumValue")
        node_ = item[0]
        node_.OperatesWith = item[1].OperatesWith

knows_query3 = """
       PREFIX vocab:      <http://www.physics-h2020.eu/physics/>

       SELECT *
       WHERE {?s  vocab:ClusterNodeIsHostedOn ?e .}"""

qres = default_world.sparql(knows_query3)

for node in onto.cluster2.ConsistsOfNodes:
    print(node.hasRamCapacity)
    print(node.hasCPUCapacity)
    print(node.ClusterNodeIsHostedOn[0].OperatesWith)

for node in onto.cluster1.ConsistsOfNodes:
    print(node.hasRamCapacity)
    print(node.hasCPUCapacity)
    print(node.ClusterNodeIsHostedOn)
    print(node.ClusterNodeIsHostedOn[0].OperatesWith)

parser_1 = getattr(r2onto, "{}_onto".format(json1_type))
parser_1(post_body[nested_json])
parser_2 = getattr(r2onto, "{}_onto".format(json2_type))
parser_2(post_body[nested_json])
parser_3 = getattr(r2onto, "{}_onto".format(json3_type))
parser_3(post_body[nested_json])