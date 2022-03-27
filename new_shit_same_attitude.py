import json

CloudProvider = "AWS"
CloudService = "VirtualServer"



with open(r"aws-describe-ec2.json", "r+") as f:
    test = json.load(f)
instances = test["Reservations"][0]["Instances"]

instances[0]["InstanceId"]
instances[0]["InstanceType"]
instances[0]["Placement"]["AvailabilityZone"]
instances[0]["PrivateIpAddress"]