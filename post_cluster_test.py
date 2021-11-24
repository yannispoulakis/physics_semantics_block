import json
import requests

'''Script to test the API'''

# sample data
data = [{"id": "cluster1",
         "name": "cluster1",
         "description": "Kubernetes cluster",
         "location": "Madrid",
         "type": "k8s",
         "so": "ubuntu18",
         "defaultNamespace": "core",
         "restAPIEndPoint": "https://192.168.1.131:16443/",
         "ip": "192.168.1.131",
         "connectionToken": "eyJhbG....wm9AKA",
         "slaLiteEndPoint": "http://localhost:8090",
         "prometheusPushgatewayEndPoint": "",
         "prometheusEndPoint": "https://192.168.1.131:9090/"
         }]

# with open('./cluster_example_input.json') as f:
#     data = json.load(f)

url = 'http://localhost:5000/add_resource/cluster'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


def post_data():
    for jsondata in data:
        res = requests.post(url, json=jsondata, headers=headers)
    print(res.json())


if __name__ == '__main__':
    post_data()
