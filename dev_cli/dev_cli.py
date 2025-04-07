#!/usr/bin/env python3

# import libraries
import click
import sys
from pathlib import Path

# =============== PATH SETUP

currentdir = Path(__file__).resolve().parent
parentdir = currentdir.parent
# add parent directory to sys.path
sys.path.insert(0, str(parentdir))

# =============== IMPORTING DOCKER MODULES

# import modules from commands.docker
from commands.docker import cleanup

# =============== IMPORTING AWS MODULES

# import modules from commands.aws
from commands.aws import s3

# =============== CLI GROUP

# define main command group for the cli tool
@click.group(help="dev-cli tool: a command-line interface for various devops utilities.")
def cli():
    """Main entry point for dev-cli Tool."""
    # function doesn't do anything.
    # is REQUIRED for defining the command group
    pass

# =============== DOCKER SUB-GROUP

# define docker command group
@click.group(help="Commands for automating docker operations.")
def docker():
    pass

# add commands to docker group
docker.add_command(cleanup.cleanup)

# =============== AWS SUB-GROUP

# define aws command group
@click.group(help="Commands for automating aws operations.")
def aws():
    pass

# add commands to docker group
aws.add_command(s3.s3)

# =============== ADD SUB-GROUPS TO MAIN CLI GROUP

# add sub-groups to the main cli group
cli.add_command(docker)
cli.add_command(aws)

# =============== SCRIPT ENTRYPOINT

# calls the cli tool if the script is executed.
if __name__ == "__main__":
    cli()