import os
import yaml
import boto3
import logging

from .utils.tags import Tags
from .utils.template import Template
from .utils.loader import Loader

level = os.environ.get("EC2_DEMO_LOG", "info").upper()
logging.basicConfig(level=level)


class Instances:

    def __init__(self, env):
        self.client = boto3.client("ec2")
        self.env = env
        self.loadEnv()


    def loadEnv(self):
        with open(f"config/{self.env}.yaml", "r") as f:
            self.vars = yaml.safe_load(f)
        logging.debug(f"self.vars: {self.vars}")


    def create(self, path: str) ->list[str]:
        ids = []
        logging.debug(f"path: {path}")
        rendered = Template.render(path, self.vars)
        data = Loader.load(rendered)

        for name, config in data["instances"].items():
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
                ids.append(instance["InstanceId"])

            return ids


    def ls(self) -> list:
        # Boto3 resources returns the ip addresses
        self.ec2 = boto3.resource("ec2")
        resources = []
        logging.debug(f"Finding ec2-demo instances...")
        res = self.ec2.instances.filter(
            Filters=[
                {
                    "Name": "tag:CreatedBy",
                    "Values": [
                        "ec2-demo",
                    ],
                },
            ],
        )

        return res


    def delete(self, ids: list[str]) -> dict:
        status = {}
        logging.debug(f"Deleting ids: {ids}")
        res = self.client.terminate_instances(
            InstanceIds=ids,
        )
        for instance in res["TerminatingInstances"]:
            status[instance["InstanceId"]] = instance["CurrentState"]["Name"]

        return status
