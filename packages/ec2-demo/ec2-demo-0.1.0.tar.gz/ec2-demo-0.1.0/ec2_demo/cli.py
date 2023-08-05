import sys
import yaml
import click
import logging

from .instances import Instances

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
    res = instances.list()
    for instance in res:
        # print(f"Instance: {instance}")
        print(f"- Instance \033[32;1m{instance['InstanceId']}\033[0m found in state \033[33;1m{instance['State']['Name']}\033[0m.")


@ec2.command()
@click.argument("env", type=str, required=True)
@click.argument("ids", type=str, required=True, nargs=-1)
def delete(env, ids):
    logging.debug(f"env: {env}")
    logging.debug(f"ids: {ids}")
    instances = Instances(env)
    status = instances.delete(ids)
    for id_, state in status.items():
        print(f"- Instance \033[32;1m{id_}\033[0m is now in state \033[32;1m{state}\033[0m.")


def main():
    ec2()


if __name__ == "__main__":
    main()
