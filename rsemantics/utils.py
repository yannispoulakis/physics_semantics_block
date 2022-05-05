import os
import json


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