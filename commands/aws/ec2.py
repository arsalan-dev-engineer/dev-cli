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
import json
from collections import defaultdict
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

# =============== CREATE COMMANDS
# ===== LIST INSTANCES

@click.command()
@click.option("-r", "--region", required=True, help="AWS region where the ec2 is located.")
def list_ec2(region):
    # initialise the ec2 client
    ec2 = boto3.client("ec2", region_name=region)
    try:
        response = ec2.describe_instances()
    except botocore.exceptions.BotoCoreError as e:
        logger.error(f"AWS Boto3 error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")    
        return
    
    # if no instances, print the message below then return
    if not response['Reservations']:
        logger.info("No ec2 instances found in your AWS account")
        return
    
    # create a dictionary to group instances by their state (e.g. running, stopped)
    grouped = defaultdict(list)

    # loop through all EC2 reservations
    for r in response.get('Reservations', []):
        # loop through all instances in each reservation
        for i in r.get('Instances', []):
            # extract tags into a dictionary (e.g., for getting the Name tag)
            tags = {t['Key']: t['Value'] for t in i.get('Tags', [])}
            # get the instance state (like 'running', 'stopped')
            state = i.get('State', {}).get('Name', 'unknown')
            # add instance details to the list under its state group
            grouped[state].append({
                'Name': tags.get('Name', 'N/A'),
                'InstanceId': i.get('InstanceId', 'N/A'),
                'InstanceType': i.get('InstanceType', 'N/A'),
                'AZ': i.get('Placement', {}).get('AvailabilityZone', 'N/A'),
                'PublicIp': i.get('PublicIpAddress', 'N/A'),
                'PrivateIp': i.get('PrivateIpAddress', 'N/A')
            })

    # print the grouped data as formatted JSON
    print(json.dumps(grouped, indent=2))
    
# ===== LAUNCH EC2 INSTANCE

@click.command()
@click.option("-r", "--region", required=True, help="AWS region where to launch ec2 instance too.")
def launch(region):
    # initialise ec2 client
    ec2 = boto3.client("ec2", region_name=region)
    
# =============== ADD COMMANDS TO GROUP

ec2.add_command(list_ec2)
ec2.add_command(launch)

if __name__ == "__main__":
   ec2()