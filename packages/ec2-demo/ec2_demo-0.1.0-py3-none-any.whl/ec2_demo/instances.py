import yaml
import boto3
import logging


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
        created = 0
        logging.debug(f"path: {path}")
        with open(path, "r") as f:
            data = yaml.safe_load(f)

        for name, config in data["instances"].items():
            logging.debug(f"name: {name}")
            logging.debug(f"config: {config}")
            logging.debug(f"spec: {config['spec']}")
            spec = config["spec"]
            spec["TagSpecifications"] = [
                {
                    "ResourceType": "instance",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": name,
                        },
                        {
                            "Key": "CreatedBy",
                            "Value": "ec2-demo",
                        },
                    ],
                },
            ]
            spec["MinCount"] = 1
            spec["MaxCount"] = 1

            logging.debug(f"Patched spec: {spec}")
            res = self.client.run_instances(**spec)

            for instance in res["Instances"]:
                logging.debug(f"InstanceId: {instance['InstanceId']}")
                ids.append(instance["InstanceId"])
                created += 1

        if created == 0:
            raise Exception("Failed to create instances")

        return ids


    def delete(self, ids: list[str]) -> dict:
        status = {}
        logging.debug(f"Deleting ids: {ids}")
        res = self.client.terminate_instances(
            InstanceIds=ids,
        )
        for instance in res["TerminatingInstances"]:
            status[instance["InstanceId"]] = instance["CurrentState"]["Name"]

        return status


    def list(self) -> list:
        resources = []
        logging.debug(f"Finding ec2-demo instances...")
        res = self.client.describe_instances(
            Filters=[
                {
                    "Name": "tag:CreatedBy",
                    "Values": [
                        "ec2-demo",
                    ],
                },
            ],
        )

        for instance in res["Reservations"][0]["Instances"]:
            resources.append(instance)
            logging.debug(f"Found instance: {instance}")

        return resources
