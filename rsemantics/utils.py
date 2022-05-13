import os
import json
import pandas as pd
import numpy as np
from rdflib import Graph, URIRef, Literal


def prepare_resources(ontology, individuals):
    graph = Graph().parse(ontology, format='xml')

    # fix individuals URIs
    for i, v in enumerate(individuals):
        individuals[i] = "http://example_composer.physics.eu/" + str(v.name)

    # put triples in pandas
    columns = ['s', 'p', 'o']
    c = 0
    data = []
    for s, p, o in graph:
        values = [s, p, o]
        zipped = zip(columns, values)
        d = dict(zipped)
        data.append(d)
    df = pd.DataFrame(data)
    df.to_csv("test_df.csv",index=False)

    # change prefix according to your prefix
    df.replace("^file:///C:/Users/giann/OneDrive/%CE%88%CE%B3%CE%B3%CF%81%CE%B1%CF%86%CE%B1/GitHub/semantics-block/registered%20clusters/", "http://example_composer.physics.eu/", regex=True,
              inplace=True)

    # df.replace("^file:///" + os.getcwd().replace("\\", "/") + "/",
           #    "http://example_composer.physics.eu/", regex=True,
            #   inplace=True)

    df.replace("^http://purl.org/linked-data/", "", regex=True, inplace=True)
    df.replace("^http://www.physics-h2020.eu/physics/", "http://www.physics-h2020.eu/physics/1.0.0/", regex=True,
               inplace=True)

    # find and drop triples from the ontology (not related to the individuals)
    df['spo'] = np.empty
    for index, row in df.iterrows():
        row['spo'] = [row['s'], row['p'], row['o']]

    drop_ind = []
    for index, row in df.iterrows():
        d = False
        for i in individuals:
            if i in row['spo']:
                d = True
        if not d:
            drop_ind.append(index)
    df.drop(set(drop_ind), inplace=True)
    df.reset_index(inplace=True)
    df = df.drop(columns=['index', 'spo'])

    # add only the relevant triples to a new graph
    g = Graph()
    for index, row in df.iterrows():
        s = URIRef(row['s'])
        p = URIRef(row['p'])
        if 'http' in row['o']:
            o = URIRef(row['o'])
        else:
            o = Literal(row['o'])
        g.add((s, p, o))

    # save the new graph
    g.serialize(destination='registered clusters/clusters1.json', format='json-ld')

    #conn.add('registered clusters/clusters1.json', base=None, format=RDFFormat.JSONLD, contexts=None)






def return_ind_id(id_db_path: str, key: str) -> str:
    with open(id_db_path, "r") as f:
        db = json.load(f)
        if key in db.keys():
            ind_name = db[key][-1].split("_")[0] + "_" + str(int(db[key][-1].split("_")[1])+1)
        else:
            ind_name = key + "_1"
        f.close()
    with open(id_db_path, "w") as f:
        db.setdefault(key, []).append(ind_name)
        f.write(json.dumps(db))
    return ind_name


def return_clust_id(id_db_path: str):
    with open(id_db_path, "r") as f:
        db = json.load(f)
    return db["Cluster"][-1]


def handleRemoveReadonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise


def cluster_already_exists(arg):
    """Deletes the input cluster from the datastore if a new one is submitted with the same name"""
    for i in onto.Cluster.instances():
        if type(arg) != str:
            if i.name == arg['name']:
                logging.info(i.name + ' already exists!')
                destroy_entity(i)  # method of owlready2
                r = True
            else:
                r = False
        elif type(arg) == str:
            if i.name == arg:
                logging.info(i.name + ' already exists!')
                destroy_entity(i)  # method of owlready2
                r = True
            else:
                r = False
    return r

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True