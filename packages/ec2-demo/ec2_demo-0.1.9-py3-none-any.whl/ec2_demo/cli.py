import click
import logging
import tabulate

from .instances import Instances
from .utils.tags import Tags


@click.group()
def ec2():
    """Manages EC2 instances"""


@ec2.command()
@click.argument("env", type=str, required=True)
@click.argument("path", type=str, required=True)
def create(env, path):
    logging.debug(f"env: {env}")
    logging.debug(f"path: {path}")
    instances = Instances(env)
    ids = instances.create(path)
    for id_ in ids:
        print(f"- Instance \033[32;1m{id_}\033[0m created.")


@ec2.command()
@click.argument("env", type=str, required=True)
def list(env):
    logging.debug(f"env: {env}")
    instances = Instances(env)
    resources = instances.ls()
    table = []
    headers = ["INSTANCE ID", "NAME", "STATE", "PRIVATE IP", "PUBLIC IP"]
    for instance in resources:
        name = Tags.find(instance.tags, "Name")
        table.append([
            instance.instance_id,
            name,
            instance.state["Name"],
            instance.private_ip_address,
            instance.public_ip_address,
        ])

    print(tabulate.tabulate(table,headers, tablefmt="rounded_outline"))


@ec2.command()
@click.argument("env", type=str, required=True)
@click.argument("ids", type=str, required=True, nargs=-1)
def delete(env, ids):
    logging.debug(f"env: {env}")
    logging.debug(f"ids: {ids}")
    inst = Instances(env)
    status = inst.delete(ids)
    for id_, state in status.items():
        print(f"- Instance \033[32;1m{id_}\033[0m is now in state \033[32;1m{state}\033[0m.")


def main():
    ec2()


if __name__ == "__main__":
    main()
