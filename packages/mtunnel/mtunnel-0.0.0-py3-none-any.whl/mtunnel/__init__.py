#!/usr/bin/env python3

import bgtunnel
import click
import dotenv
import os
import requests
import socket
import subprocess
import sys
import time
import yaml

from dotenv import load_dotenv


load_dotenv()

ON_POSIX = 'posix' in sys.builtin_module_names


def get_open_port():
    with socket.socket() as s:
        s.bind(('', 0))
        return s.getsockname()[1]


@click.command()
@click.pass_context
@click.argument('project')
@click.argument('stage')
@click.option('--config', default='mtunnel.yml')
def main(ctx: click.Context, project: str, stage: str, config: str):
    with open(config, 'r') as f:
        config = yaml.safe_load(f)

    if project not in config['projects']:
        click.echo('Project not found')
        ctx.exit(1)

    project = config['projects'][project]

    if stage not in project['stages']:
        click.echo('Stage not found in project')
        ctx.exit(1)

    stages = project['stages'][stage]
    jumpbox = config['jumpbox']

    for connection_id, connection in stages.items():
        enabled = connection.pop('enabled', True)

        if enabled:
            kwargs = {
                **jumpbox,
                **connection,
            }

            connection['forwarder'] = bgtunnel.open(**kwargs)

    while True:
        time.sleep(0.5)
