"""
EC2 Instance Manager

Automate common AWS EC2 tasks such as launching, listing, starting, stopping, 
and terminating instances, as well as managing AMIs, volumes, and tags through a 
user-friendly CLI interface.

Usage:
    dev-cli AWS EC2 [COMMANDS]

Commands:
    launch         Launch a new EC2 instance with specified configuration.
    list           List all EC2 instances with their state and metadata.
    status         Get the status of an EC2 instance.
    start          Start a stopped EC2 instance.
    stop           Stop a running EC2 instance.
    reboot         Reboot an EC2 instance.
    terminate      Terminate an EC2 instance.
    tag            Add or modify tags on EC2 instances.
"""

# import libraries
import boto3.exceptions
import boto3
import botocore.exceptions
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
# ===== DESCRIBE INSTANCES

@click.command(help="Show detailed metadata of EC2 instances in a region.")
@click.option("-r", "--region", help="AWS region.")
@click.option("-s", "--state", help="Filter instances by state (e.g., running, stopped).")
def describe(region, state):
    # Initialise EC2 client
    ec2 = boto3.client("ec2", region_name=region)
    
    try:
        response = ec2.describe_instances()
    except botocore.exceptions.BotoCoreError as e:
        logger.error(f"AWS Boto3 error: {e}")
        return
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return

    if not response['Reservations']:
        logger.info("No EC2 instances found in your AWS account.")
        return

    grouped = defaultdict(list)

    # Loop through reservations and instances
    for reservation in response.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            inst_state = instance.get('State', {}).get('Name', 'unknown')
            
            # Filter by state if provided
            if state and inst_state != state:
                continue

            tags = {t['Key']: t['Value'] for t in instance.get('Tags', [])}
            grouped[inst_state].append({
                'Name': tags.get('Name', 'N/A'),
                'InstanceId': instance.get('InstanceId', 'N/A'),
                'InstanceType': instance.get('InstanceType', 'N/A'),
                'AZ': instance.get('Placement', {}).get('AvailabilityZone', 'N/A'),
                'PublicIp': instance.get('PublicIpAddress', 'N/A'),
                'PrivateIp': instance.get('PrivateIpAddress', 'N/A')
            })

    # Sort instances in each state by Name
    for state_group in grouped:
        grouped[state_group] = sorted(grouped[state_group], key=lambda x: x['Name'])

    if not any(grouped.values()):
        logger.info(f"No EC2 instances found in state: {state}")
        return

    # Output result as pretty-printed JSON
    print(json.dumps(grouped, indent=4))    

# ===== TERMINATE EC2 INSTANCE

@click.command(help="Terminate a specific EC2 instance by instance ID.")
@click.option("-i", "--instance-id", required=True, help="ID of the EC2 instance to terminate.")
@click.option("-r", "--region", required=True, help="AWS region where the EC2 instance is located.")
@click.option("--yes", is_flag=True, help="Skip confirmation prompt before termination.")
def terminate(instance_id, region, yes):
    ec2 = boto3.client('ec2', region_name=region)

    # Step 1: Check if the instance exists and retrieve its state
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]
        current_state = instance['State']['Name']

        # step 2: If the instance is already terminated, don't prompt for termination
        if current_state == 'terminated':
            logger.info(f"Instance {instance_id} is already terminated")
            return

        # step 3: Only prompt for termination if it's in a valid state (running, stopped, etc.)
        if not yes:
            confirm = input(f"Are you sure you want to terminate instance '{instance_id}'? Current state: {current_state} [y/N]: ")
            if confirm.strip().lower() != 'y':
                logger.info("Termination cancelled by user.")
                return

        # step 4: Proceed with termination
        terminate_response = ec2.terminate_instances(InstanceIds=[instance_id])

        instance_info = terminate_response["TerminatingInstances"][0]
        state = instance_info["CurrentState"]["Name"]
        previous_state = instance_info["PreviousState"]["Name"]

        logger.info(f"Termination initiated for instance: {instance_id}. Current state: {state}")
        
        # step 5: Print the response as clean JSON
        output = {
            "InstanceId": instance_id,
            "CurrentState": state,
            "PreviousState": previous_state
        }
        print(json.dumps(output, indent=4))

    # exception handling
    except botocore.exceptions.ClientError as e:
        logger.error(f"AWS ClientError: {e.response['Error']['Message']}")
    except botocore.exceptions.BotoCoreError as e:
        logger.error(f"BotoCoreError: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

# ===== LAUNCH EC2 INSTANCE

@click.command(help="Launche an EC2 instance in a specifed region.")
@click.option("-a", "ami-id", required=True, help="AMI id to launch the EC2 instance with.")
@click.option("-t", "--instance-type", default="t2.micro", show_default=True, help="Ec2 instance type to launch.")
@click.option("-k", "--key-name", required=True, help="Name of the key pair to use.")
@click.option("-r", "--region", default="eu-west-2", show_default=True, help="AWS region where to launch EC2 instance too.")
def launch(region):
    # initialise EC2 client
    ec2 = boto3.client("ec2", region_name=region)
    
# =============== ADD COMMANDS TO GROUP

ec2.add_command(describe)
ec2.add_command(launch)
ec2.add_command(terminate)

if __name__ == "__main__":
   ec2()