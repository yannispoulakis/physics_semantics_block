from owlready2 import destroy_entity, get_ontology
import ontospy.cli
from owlready2 import default_world
from datetime import datetime
from uuid import uuid4

from rsemantics.utils import return_ind_id


class r2onto:
    """A class that is comprised of methods that parse certain filetypes that describe a cluster setting (Platform,
    Nodes, Node-Hosts). After parsing the respective ontology individuals are created along with their respective
    extracted data properties."""

    def __init__(self, onto_path="resource_ontology.owl"):
        self.onto = get_ontology(onto_path).load()
        self.cluster = ''
        self.host_resource = ''
        self.architecture = ''
        self.cloud_platforms = ["OpenShift", "Kubernetes"]
    def ec2_onto(self, instances):
        """parses the output of aws describe instances. An example of the output can be found here :
        https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html"""

        instances = instances["Reservations"][0]["Instances"]

        # The names of the individuals are defined according to the return_ind_id function
        cp = self.onto.CloudProvider(return_ind_id("static/ontology_resource_individuals_id.json", "CloudProvider"))
        cs = self.onto.CloudService(return_ind_id("static/ontology_resource_individuals_id.json", "CloudService"))
        cp.providesCloudService = [cs]
        cs.CloudServiceLocation = instances[0]["Placement"]["AvailabilityZone"]
        cs.CloudServiceInstanceID = [instances[0]["InstanceId"]]
        cs.CloudServicePrivateIP = [instances[0]["PrivateIpAddress"]]
        cs.CloudServiceInstanceType = [instances[0]["InstanceType"]]

        self.architecture = instances[0]["Architecture"]
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
        ct = self.onto.Cluster(return_ind_id("static/ontology_resource_individuals_id.json", "Cluster"))
        # ID is manually generated
        ct.hasID = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())


        if clusterdesc["platform"] in self.cloud_platforms:
            plt = self.onto.CloudPlatform(clusterdesc["platform"])
        plt.PlatformHasDistribution = clusterdesc["distribution"]
        ct.ClusterUsesPlatform = plt
        self.cluster = ct

        # Cluster Objectives Temporarily hard coded.
        if clusterdesc["distribution"] == "K3s":
            ct.hasEnergyScore = 60
            ct.hasResilienceScore = 10
            ct.hasPerformanceScore = 20
        else:
            ct.hasEnergyScore = 40
            ct.hasResilienceScore = 15
            ct.hasPerformanceScore = 30

    def nodes_onto(self, nodedesc):
        for node in nodedesc["items"]:
            nd = self.onto.ClusterNode(return_ind_id("static/ontology_resource_individuals_id.json", "ClusterNode"))
            # Assign Role to the node (Master/Worker)
            if "node-role.kubernetes.io/worker" in node["metadata"]["labels"].keys():
                nd.hasRole = "Worker"
            else:
                nd.hasRole = 'Master'

            # Node Operating System - Architecture and image
            ops = self.onto.OperatingSystem(return_ind_id("static/ontology_resource_individuals_id.json", "OS"))
            ops.hasImage = node["status"]["nodeInfo"]["osImage"]
            ops.hasArchitecture = node["status"]["nodeInfo"]["architecture"]
            nd.operatesWith = ops

            # Ram and CPU
            ram = self.onto.Ram(return_ind_id("static/ontology_resource_individuals_id.json", "Ram"))
            ram.withAllocatableValue = node["status"]["allocatable"]["memory"]
            ram.withCapacityValue = node["status"]["capacity"]["memory"]
            cpu = self.onto.CPU(return_ind_id("static/ontology_resource_individuals_id.json", "CPU"))
            cpu.withAllocatableValue = node["status"]["allocatable"]["cpu"]
            cpu.withCapacityValue = node["status"]["capacity"]["cpu"]
            nd.hasRawComputationalResource = [ram, cpu]

    def connect_classes(self):
        # Connect Clusters with their nodes
        if self.cluster == "":
            return
        self.cluster.ConsistsOfNodes = [x for x in list(self.onto.individuals()) if
                                        x.__class__ == self.onto.ClusterNode]  # Won't work for two clusters in 1 graph
        # Host of Nodes
        for node in [x for x in list(self.onto.individuals()) if x.__class__ == self.onto.ClusterNode]:

            node.ClusterNodeIsHostedOn = [self.host_resource]
        self.cluster.hasArchitecture = self.architecture