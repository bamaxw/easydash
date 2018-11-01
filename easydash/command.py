#!/usr/bin/env python3
from .cli import map_resource
from helpers.args import ArgParser


def main():
    args = ArgParser()
    resource_type = args.register('resource_type', named=False)
    command = args.register('command', named=False)
    region = args.register('region', default='eu-west-1')
    args.validate()

    resource = map_resource.get(resource_type)
    if resource is None:
        raise ValueError(f"Can't recognize resource {resource}")
    command_func = resource.map_command(command)
    args = resource.get_args()
    kwargs = resource.get_kwargs()
    return command_func(*args, **kwargs)
