from owlready2 import destroy_entity, get_ontology
import ontospy.cli
from owlready2 import default_world
from datetime import datetime
from uuid import uuid4

class r2onto:
    def __init__(self, onto_path="physics_ontology_v12.owl"):
        self.onto = get_ontology(onto_path).load()
        self.cluster = ""
        self.host_resource = ''
        return

    def ec2_onto(self, instances):
        instances = instances["Reservations"][0]["Instances"]
        cp = self.onto.CloudProvider("AWS")
        cs = self.onto.Cloud_Service("EC2")
        cp.providesCloudService = [cs]
        cs.CloudServiceLocation = instances[0]["Placement"]["AvailabilityZone"]
        cs.CloudServiceInstanceID = [instances[0]["InstanceId"]]
        cs.CloudServicePrivateIP = [instances[0]["PrivateIpAddress"]]
        cs.CloudServiceInstanceType = [instances[0]["InstanceType"]]
        self.host_resource = cs


    def rpi_onto(self, rpi_info):
        for runit in rpi_info["items"]:
            unit = self.onto.SingleBoardUnit()

            ram = self.onto.Ram()
            ram.withNumValue = runit["memory"]["total"]

            cpu = self.onto.CPU()
            cpu.withNumValue = runit["cpu"]["cores"]

            unit.OperatesWith = self.onto.Linux()
            unit.hasRawComputationalUnit = [ram, cpu]
            self.host_resource = unit


    def cluster_onto(self, clusterdesc):
        ct = self.onto.Cluster()
        ct.ClusterHasID = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
        #ct.ClusterHasID = clusterdesc["items"][0]["spec"]["clusterID"]
        # plt = self.onto.OpenShift()
        plt = getattr(self.onto, clusterdesc["platform"])()
        plt.PlatformHasDistribution = clusterdesc["distribution"]
        ct.ClusterUsesPlatform = plt
        self.cluster = ct


    def nodes_onto(self, nodedesc):
        for node in nodedesc["items"]:
            os = self.onto.OS()
            os.OperatingSystemHasImage = [node["status"]["nodeInfo"]["osImage"]]
            os.OperatingSystemHasArchitecture = [node["status"]["nodeInfo"]["architecture"]]

            nd = self.onto.ClusterNode()
            if "node-role.kubernetes.io/worker" in node["metadata"]["labels"].keys():
                nd.hasRole = "Worker"
            else:
                nd.hasRole = 'Master'

            nd.OperatesWith = os


            # Ram and CPU
            ram = self.onto.Ram()

            ram.RawComputationalResourceAllocatableValue = node["status"]["allocatable"]["memory"]
            ram.RawComputationalResourceCapacityValue = node["status"]["capacity"]["memory"]
            cpu = self.onto.CPU()
            cpu.RawComputationalResourceAllocatableValue = node["status"]["allocatable"]["cpu"]
            cpu.RawComputationalResourceCapacityValue = node["status"]["capacity"]["cpu"]

            nd.ClusterNodeHasComputationalUnit = [ram, cpu]

    def connect_classes(self):
        self.cluster.ConsistsOfNodes = [x for x in list(self.onto.individuals()) if
                              x.__class__ == self.onto.ClusterNode]  # edw mporei na mhn pai3ei me 2o cluster

        for node in [x for x in list(self.onto.individuals()) if  x.__class__ == self.onto.ClusterNode]:
            print(node)
            node.ClusterNodeIsHostedOn = [self.host_resource]