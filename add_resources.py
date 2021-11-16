from owlready2 import * 
import os 
from flask import Flask, request, render_template
import yaml
from tosca_for_physics import TOSCAForPHYSICS
import io


workdir = os.getcwd()

def load_ontology(filepath="physics.owl"): 
    "This functions loads the PHYSICS ontology either by loading the default one or reading a user-submitted.""" 
    workdir = os.getcwd()
    ontology = get_ontology(filepath).load()
    return ontology 


def parse_resource(input_json,ontology):
    """ param input_json:  A json containing information on certain resources
        type input json : json """
    