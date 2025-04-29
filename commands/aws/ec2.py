"""
EC2 Instance Manager

Automate common AWS EC2 tasks such as launching, listing, starting, stopping, 
and terminating instances, as well as managing AMIs, volumes, and tags through a 
user-friendly CLI interface.

Usage:
    dev-cli aws ec2 [COMMANDS]

Commands:
    launch         Launch a new EC2 instance with specified configuration.
    list           List all EC2 instances with their state and metadata.
    status         Get the status of an EC2 instance.
    start          Start a stopped EC2 instance.
    stop           Stop a running EC2 instance.
    reboot         Reboot an EC2 instance.
    terminate      Terminate an EC2 instance.
    tag            Add or modify tags on EC2 instances.

    create-ami     Create an AMI from an existing EC2 instance.
    list-amis      List AMIs owned by your AWS account.
    del-ami        Deregister a specified AMI.

    attach-volume  Attach an EBS volume to an EC2 instance.
    detach-volume  Detach an EBS volume from an EC2 instance.
    list-volumes   List EBS volumes in your account.
"""

# import libraries
import boto3.exceptions
import boto3
import click
import sys
from pathlib import Path
import botocore
import logging
import json
from botocore.exceptions import BotoCoreError, ClientError

# =============== PATH SETUP

# add parent directory to sys.path to support local imports (if any)
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.insert(0, (parent_dir))

# =============== LOGGING SETUP

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s."
)
logger = logging.getLogger(__name__)

# =============== CLI GROUP SETUP

@click.group(help="A CLI tool to automate AWS EC2 operations.")
@click.option("--verbose", is_flag=True, help="Enable verbose output.")
@click.option("--log-level", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False), default="INFO", help="Set the logging level.")
def ec2(verbose, log_level):
    log_level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(log_level)
    if verbose:
      logger.debug("Verbose mode enabled.")

# =============== ADD COMMANDS TO EC2 GROUP

if __name__ == "__main__":
   ec2()