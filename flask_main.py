from flask import Flask, request, render_template
from owlready2 import *

onto = get_ontology("physics.owl").load()
onto.base_iri

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
    global cluster_instance
    cluster_instance = onto.Cluster()
    for item in list(onto.data_properties()):
        if item.domain == onto.Cluster:
            setattr(cluster_instance, item.name, arg[item.name])

    return "Individual created"


@app.route("/get_individuals", methods=["POST"])
def get_individuals():
    """Receive json input via POST requests and store them server-side"""
    arg = request.get_json()
    for i in onto.Cluster.instances():
        print(i)

    return "Individual created"


if __name__ == "__main__":
    app.run()
