import json
from flask import Flask, request, render_template
from owlready2 import *
from static_params import cluster_properties
import logging
import ontospy
from ontospy.ontodocs.viz.viz_d3dendogram import *

onto = get_ontology("physics_V0.1.owl").load()
onto.base_iri


def cluster_already_exists(arg):
    """Deletes the input cluster from the datastore"""
    for i in onto.Cluster.instances():
        if i.name == arg['name']:
            logging.info(i.name + ' already exists!')
            destroy_entity(i)
            r = True
        else:
            r = False
    return r


app = Flask(__name__)


@app.route("/")
def render_home():
    return render_template("main_page.html")


@app.route("/add_resource", methods=["POST"])
def parse_resource_input():
    """Receive json input via POST requests and store them server-side"""
    arg = request.get_json()
    print(arg)
    return "resource added!"


@app.route("/add_resource/cluster", methods=["POST"])
def parse_cluster_input():
    """Receive json input via POST requests and store them server-side"""
    arg = request.get_json()
    # global cluster_instance
    cluster_instance = onto.Cluster()
    if cluster_already_exists(arg):
        logging.info('Updating ' + arg['name'])
    for item in list(onto.data_properties()):
        if onto.Cluster in item.domain:
            # check whether the POSTed data have info for all the cluster data properties
            if item.name in arg:
                setattr(cluster_instance, item.name, arg[item.name])
                logging.info(cluster_instance.get_name() + ' saved', )
    return json.dumps(cluster_instance.get_name() + ' saved')


@app.route("/get_individuals", methods=["POST"])
def get_individuals():
    """Receive json input via POST requests and store them server-side"""
    arg = request.get_json()
    for i in onto.Cluster.instances():
        print(i)

    return "Individual created"


@app.route("/get_available_clusters", methods=["GET"])
def get_available_clusters():
    """Returns in json information about the available clusters"""
    d = dict()
    for i in onto.Cluster.instances():
        d[i.name] = i.__dict__
        # keep only the relevant properties for each cluster
        d[i.name] = {k: v for k, v in d[i.name].items() if k in cluster_properties}
    return d

@app.route("/visualize_ontology", methods=["GET"])
def visualize_ontology():
    """Provides a visualization of the ontology with ontospy"""
    from shutil import copyfile
    from distutils.dir_util import copy_tree

    g = ontospy.Ontospy("physics_V0.1.owl")
    v = Dataviz(g)  # => instantiate the visualization object
    d3_result = v.build("dendrogram/")  # => render visualization. You can pass an 'output_path' parameter too
    copy_tree("dendrogram/static", r"C:\Users\giann\OneDrive\Έγγραφα\GitHub\physics_semantics_block\static")
    copyfile("dendrogram/index.html", r"C:\Users\giann\OneDrive\Έγγραφα\GitHub\physics_semantics_block\templates\index.html")

    return render_template("index.html")

if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=False)
