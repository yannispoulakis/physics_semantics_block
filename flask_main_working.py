from rsemantics.utils import is_json, prepare_resources
from rsemantics.r2onto import r2onto
from rsemantics.SemanticRules import service_onto_rules

from flask import Flask, request, render_template, Response

from owlready2 import *
import logging
import ontospy
from ontospy.ontodocs.viz.viz_d3dendogram import *
import errno, os, stat, shutil

#onto = get_ontology("physics_ontology_v12.owl").load()
app = Flask(__name__)



@app.route("/")
def render_home():
    """Home page"""
    return render_template("/main/home.html")


"""Ontology Documentation and description pages"""


@app.route("/ontology-documentation", methods=["GET"])
def ontology_documentation():
    """Renders the home page of the ontology documentation as produced by ontospy."""
    return render_template("index.html")


@app.route("/<html>")
def dynamic_route(html):
    if html == "favicon.ico":
        return render_template("main/home.html")
    """Renders html dynamically. Mostly used to render the pages produced by ontospy"""
    return render_template("{}".format(html))


@app.route("/register-resource", methods=['GET', 'POST'])
def register_resource():
    """Registers a new cluster. The input body should consist of three different jsons"""

    if request.method == "GET":
        return render_template('main/resource_registration_visual.html')

    if request.method == "POST":
        if is_json(request.get_data()):
            pass
        else:
            return "422 - Unprocessable Entity"
        r2 = r2onto()

        # Read request parameters and body
        json1_type = request.args.get('1')
        json2_type = request.args.get('2')
        json3_type = request.args.get('3')
        nested_json_types = [json1_type, json2_type, json3_type]
        post_body = request.get_json()

        for idx, nested_json in enumerate(post_body):
            parser = getattr(r2, "{}_onto".format(nested_json_types[idx]))
            parser(post_body[nested_json])

        r2.connect_classes()
        r2.onto.save("cluster_ontology", format="rdfxml")

        sr = service_onto_rules(r2.onto)
        sr.add_locality()

        print(r2.onto.cluster1.hasLocality)

        return "200"


@app.route("/api/register-resource", methods=['GET', 'POST'])
def register_resource_api():
    """Registers a new cluster. The input body should consist of three different jsons"""

    if request.method == "GET":
        return "The API route for registering a cluster."

    if request.method == "POST":
        if is_json(request.get_data()):
            pass
        else:
            return "422 - Unprocessable Entity"

        r2 = r2onto()

        # Read request parameters and body
        json1_type = request.args.get('1')
        json2_type = request.args.get('2')
        json3_type = request.args.get('3')
        nested_json_types = [json1_type, json2_type, json3_type]
        post_body = request.get_json()

        for idx, nested_json in enumerate(post_body):
            parser = getattr(r2, "{}_onto".format(nested_json_types[idx]))
            parser(post_body[nested_json])

        r2.connect_classes()
        r2.onto.save("cluster_ontology", format="rdfxml")

        sr = service_onto_rules(r2.onto)
        sr.add_locality()

        r2.onto.save("registered clusters/cluster_ontology", format="rdfxml")
        prepare_resources("registered clusters/cluster_ontology", list(r2.onto.individuals()))
        print(r2.cluster.hasLocality)

        return "200"


@app.route("/ontology-raw", methods=['GET', 'POST'])
def onto_raw():
    with open("physics_ontology_v12.owl", "r", encoding="utf8") as f:
        data = f.read()

    for line in data:
        print(line)
        break
    return Response(data, mimetype="text/xml")


if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=False)