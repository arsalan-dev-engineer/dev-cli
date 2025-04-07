"""
S3 Bucket Manager

Automate common AWS S3 tasks such as creating, listing, deleting, uploading, syncing,
and managing bucket policies using a clean CLI interface.

Usage:
    dev-cli aws s3 [COMMANDS]

Commands:
    create         Create a new S3 bucket.
    delete         Delete an existing S3 bucket.
    upload         Upload files to an S3 bucket.
    download       Download files from an S3 bucket.
    sync           Sync a local folder with an S3 bucket.
    buckets        List all S3 buckets.
    ls             List objects within a specified S3 bucket.
    set-policy     Apply a bucket policy to a specific S3 bucket.
    get-policy     View the current policy of an S3 bucket.
    del-policy  Delete a bucket policy from a specified S3 bucket.
"""

import boto3.exceptions
import botocore
import click
import sys
from pathlib import Path
import boto3
import botocore
from botocore.exceptions import ClientError
from rich.logging import RichHandler
import logging
import json

# =============== PATH SETUP


# add parent directory to sys.path to support local imports (if any)
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.insert(0, (parent_dir))

# =============== LOGGING SETUP


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s.")
logger = logging.getLogger(__name__)

# =============== CLI GROUP SETUP


@click.group(help="A CLI tool to automate AWS S3 operations.")
@click.option("--verbose", is_flag=True, help="Enable verbose output.")
@click.option("--log-level", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False), default="INFO", help="Set the logging level.")
def s3(verbose, log_level):
    log_level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(log_level)
    if verbose:
        logger.debug("Verbose mode enabled.")

# =============== CLI COMMANDS
# =============== CREATE S3 BUCKET


@click.command(help="Create a new S3 bucket in the specified AWS region.")
@click.option("-bn", "--bucket-name", required=True, help="The name of the bucket to create.")
@click.option("-r", "--region", required=True, help="The AWS region where the bucket will be created (e.g., 'us-west-2').")
def create(bucket_name, region):
    """Create an S3 bucket with the given name in the specified region."""
    # initalise the S3 client for the given region
    s3_client = boto3.client('s3', region_name=region)
    # bucket config required for non-default regions
    # specifies the AWS region where the S3 bucket will be created
    config = {'LocationConstraint': region}

    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration=config
        )
        logging.info(
            f"S3 bucket '{bucket_name}' created successfully in region: '{region}'")
    except boto3.exceptions.Boto3Error as e:
        logging.error(f"Failed to create bucket: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occured: {e}")

# =============== DELETE S3 BUCKET


@click.command(help="Delete an existing S3 bucket.")
@click.option("-bn", "--bucket-name", required=True, help="The name of the bucket to delete.")
@click.option("-r", "--region", required=True, help="The AWS region where the bucket will be deleted from (e.g., 'eu-west-2').")
def delete(bucket_name, region):
    # create an S3 client in the specified region
    s3 = boto3.client('s3', region_name=region)
    try:
        # delete S3 bucket
        s3.delete_bucket(Bucket=bucket_name)
        logger.info(
            f"Bucket '{bucket_name}' successfully deleted from region '{region}'")
    # hand aws client-side errors
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error'].get(
            "Message", "No error message provided.")
        logger.error(f"AWS ClientError [{error_code}]: {error_message}")

    # handle boto3 related errors
    except botocore.exceptions.BotoCoreError as e:
        logger.error(f"BotoCoreError: {e}")
    # handle any other unexpected exceptions
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

# INCOMPLETE ==========


@click.command(help="Upload a file or directory to an S3 bucket.")
def upload():
    pass

# INCOMPLETE ==========


@click.command(help="Download a file or folder from an S3 bucket.")
def download():
    pass

# INCOMPLETE ==========


@click.command(help="Sync a local directory with an S3 bucket.")
def sync():
    pass

# =============== LIST ALL S3 BUCKETS


@click.command(help="List all S3 buckets in your AWS account.")
def buckets():
    # initialize the S3 client
    s3 = boto3.client('s3')

    try:
        # fetch the list of S3 buckets
        response = s3.list_buckets()
    except botocore.exceptions.BotoCoreError as e:
        logger.error(f"AWS Boto3 error: {e}")
        return
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return

    # if no buckets exist, notify the user and exit
    if not response['Buckets']:
        logger.info("No S3 buckets found in your AWS account.")
        return

    logger.info("Existing S3 buckets:")
    # enumerate through each bucket and print its name and creation date
    for idx, bucket in enumerate(response['Buckets'], 1):
        # fallback in case 'Name' is missing
        name = bucket.get('Name', 'Unnamed')
        # get creation date if available
        created = bucket.get('CreationDate')
        created_str = created.strftime(
            '%Y-%m-%d %H:%M:%S') if created else 'Unknown date'
        logger.info(f"\t{idx}: {name}\n\t   └─ Created on: {created_str}")

# =============== LIST OBJECTS IN S3 BUCKET


@click.command(help="List objects inside a specific S3 bucket.")
@click.option("-bn", "--bucket-name", required=True, help="Name of the bucket to list objects from.")
@click.option("-r", "--region", required=True, help="AWS region where the bucket is located.")
def ls(bucket_name, region):
    # initialise the S3 client
    s3 = boto3.client('s3', region_name=region)
    try:
        # attempt to list objects inside that specified bucket
        response = s3.list_buckets_v2(Bucket=bucket_name)
        if 'Contents' not in response:
            logger.info(f"No objects found in bucket '{bucket_name}'.")
            return

        logger.info(f"Objects in bucket '{bucket_name}':")
        for obj in response['Contents']:
            key = obj['Key']
            size = obj['Size']
            last_modified = obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S')
            logger.info(
                f"  ├─ {key} | {size} bytes | Last modified: {last_modified}")

    # handle specified aws client-side errors
    except botocore.exceptions.ClientError as E:
        error_code = e.response['Error']['Code']
        logger.error(
            f"AWS ClientError [{error_code}]: {e.response['Error'].get('Message', '')}")
    # handle any other unexpected errors
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

# INCOMPLETE ==========


@click.command(help="Apply a policy to a specified S3 bucket.")
def set_policy():
    pass

# =============== GET S3 BUCKET POLICY


@click.command(help="Retrieve and display the current policy of a bucket.")
@click.option("-bn", "--bucket-name", required=True, help="Input the name of the existing bucket.")
def get_policy(bucket_name):
    s3 = boto3.client('s3')
    try:
        response = s3.get_bucket_policy(Bucket=bucket_name)
        policy = response['Policy']
        # pretty-print the bucket policy JSON
        logger.info(
            f"Policy for bucket '{bucket_name}':\n{json.dumps(json.loads(policy), indent=2)}")
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchBucketPolicy':
            logger.warning(f"No policy attached to bucket '{bucket_name}'.")
        else:
            logger.error(
                f"Unable to retrieve policy for bucket '{bucket_name}': {e}")
        # only return on exception
        return

# =============== DELETE S3 BUCKET POLICY


@click.command(help="Delete a policy from a specified S3 bucket.")
def del_policy():
    pass

# =============== ADDING COMMANDS TO GROUPS


# Bucket management commands
s3.add_command(create)
s3.add_command(delete)
# lists all buckets
s3.add_command(buckets)
s3.add_command(ls)

# object operations
s3.add_command(upload)
s3.add_command(download)
s3.add_command(sync)

# policy management
s3.add_command(set_policy)
s3.add_command(get_policy)
s3.add_command(del_policy)

# =============== SCRIPT ENTRYPOINT


if __name__ == "__main__":
    s3()
