import boto3
import logging
import time

from .utils.tags import Tags


class Task:

    def __init__(self, vars):
        self.vars = vars
        self.client = boto3.client("ec2")
        self.instanceIds = []

    def create(self, name: str, config: dict) ->list[str]:
        envTags = self.vars["tags"]
        envTags.update({"Name": name})
        awsTags = Tags.build(envTags)

        logging.debug(f"Name: {name}")
        logging.debug(f"Config: {config}")
        logging.debug(f"Spec: {config['spec']}")
        spec = config["spec"]
        spec["TagSpecifications"] = [
            {
                "ResourceType": "instance",
                "Tags": awsTags,
            },
        ]
        spec["MinCount"] = 1
        spec["MaxCount"] = 1

        logging.debug(f"Patched spec: {spec}")
        res = self.client.run_instances(**spec)

        for instance in res["Instances"]:
            logging.debug(f"InstanceId: {instance['InstanceId']}")
            self.instanceIds.append(instance["InstanceId"])

        time.sleep(2)
        return self.instanceIds
