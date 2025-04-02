
# import libraries
import click
import sys
from pathlib import Path
import docker

# get current directory
current_dir = Path(__file__).resolve().parent
# get parent directory
parent_dir = current_dir.parent
# add parent directory to sys.path
sys.path.insert(0, str(parent_dir))

client = docker.from_env()

@click.group(help="A cli tool to clean up unused Docker resources.")
def clean():
    """
    Group of commands for Docker resource cleanup.
    """
    pass

@click.command("clean")
@click.option()
@click.option()
@click.option()
def docker_cleanup():
    pass