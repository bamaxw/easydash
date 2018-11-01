#!/usr/bin/env python3
from helpers.args import ArgParser
from .cli import map_resource
import json


def main():
    args = ArgParser('dash')
    resource_type = args.register('resource_type', named=False)
    command = args.register('command', named=False)
    region = args.register('region', default='eu-west-1')
    args.validate()

    resource = map_resource.get(resource_type)
    if resource is None:
        raise ValueError(f"Can't recognize resource {resource}")
    cmd_func = resource.map_command(command)
    cmd_args = resource.get_args()
    cmd_kwargs = resource.get_kwargs()
    val = cmd_func(*cmd_args, **cmd_kwargs)
    print(json.dumps(val))
