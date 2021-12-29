from owlready2 import *

onto = get_ontology("physics_V0.1.owl").load()
onto.base_iri
clust = onto.Cluster()

"""Individuals and Classes have the is_a property that returns the superclasses"""
print("Superclasses of the Cluster class are: {}".format(onto.Cluster.is_a))
print("Classes of the Cluster individual are: {}".format(clust.is_a))

"""Data properties"""
print("The data properties of the ontology are: {}".format(list(onto.data_properties())))

for item in list(onto.data_properties()):
    print(item)
    print(item.domain)
    if onto.Cluster in item.domain:
        print("ok")
    else:
        print("asd")








