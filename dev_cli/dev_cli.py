#!/usr/bin/env python3

# =============== IMPORTING MODULES

from commands.docker import cleanup
from commands.aws import s3
from commands.aws import ec2
import click
import sys
from pathlib import Path
from commands.toolkit import cache
from commands.automations import random_api
from commands.automations.finhub import stocks


# =============== PATH SETUP

currentdir = Path(__file__).resolve().parent
parentdir = currentdir.parent
# add parent directory to sys.path
sys.path.insert(0, str(parentdir))

# =============== CLI MAIN GROUP

# define main command group for the cli tool
@click.group(help="dev-cli tool: a command-line interface for various devops utilities.")
def cli():
    """Main entry point for dev-cli Tool."""
    # function doesn't do anything.
    # is REQUIRED for defining the command group
    pass

# =============== SUB-GROUPS

# define aws command group
@click.group(help="Commands for automating aws operations.")
def aws():
    pass

# define docker command group
@click.group(help="Commands for automating Docker container operations.")
def docker():
    pass

# define docker command group
@click.group(help="Commands for automating DevOps operations.")
def toolkit():
    pass

@click.group(help="Commands for automation scripts.")
def automations():
    pass

# inside automations command
@click.group(help="Commands for finance-related automation tasks.")
def finhub():
    pass

# =============== ADD SUB-GROUPS TO MAIN CLI GROUP

# add sub-groups to the main cli group
cli.add_command(aws)
cli.add_command(docker)
cli.add_command(toolkit)
cli.add_command(automations)
automations.add_command(finhub)

# =============== ADD COMMANDS TO SUB-GROUPS

# commands/aws
aws.add_command(s3.s3)
aws.add_command(ec2.ec2)

# commands/docker
docker.add_command(cleanup.cleanup)

# commands/toolkit
toolkit.add_command(cache.cache)

# commands/automations
automations.add_command(random_api.random_api)

# commands/automations/finhub
finhub.add_command(stocks.stocks)

# =============== SCRIPT ENTRYPOINT

# calls the cli tool if the script is executed.
if __name__ == "__main__":
    cli()
