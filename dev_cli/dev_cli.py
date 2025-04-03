#!/usr/bin/env python3

# import libraries
import click
import sys
from pathlib import Path

# get current script directory
currentdir = Path(__file__).resolve().parent
# get parent directory
parentdir = currentdir.parent
# add parent directory to sys.path
sys.path.insert(0, str(parentdir))

# import modules from commands.personal directory
from commands import docker_cleanup

# define main command group for the CLI Tool
@click.group(help="dev-cli tool: a command-line interface for various devops utilities.")
def cli():
    """Main entry point for dev-cli Tool."""
     # function doesn't do anything.
     # is REQUIRED for defining the command group
    pass

cli.add_command(docker_cleanup.docker_cleanup)

# entry point of the script.
# calls the cli tool if the script is executed.
if __name__ == "__main__":
    cli()