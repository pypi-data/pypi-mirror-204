import logging
import boto3


class Task:

    def run(self, name: str, config: dict):
        self.name = name
        self.config = config

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
