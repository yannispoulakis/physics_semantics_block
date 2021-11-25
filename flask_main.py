import json
from flask import Flask, request, render_template
from owlready2 import *
from static_params import cluster_properties
import logging
onto = get_ontology("physics.owl").load()
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


@app.route("/get_locations_of_available_clusters", methods=["GET"])
def get_locations_of_available_clusters():
    """Returns in json geolocation information about the available clusters"""
    d = dict()
    for i in onto.Cluster.instances():
        d[i.name] = i.location
        # keep only the relevant properties for each cluster
        #d[i.name] = {k: v for k, v in d[i.name].items() if k in "location"}
    return d


if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
