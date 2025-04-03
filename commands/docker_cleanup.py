
"""
A CLI tool to clean up unused Docker resources.

This tool helps you remove unused Docker resources like containers, images, volumes, and networks.
You can preview what would be deleted with the --dry-run flag and skip confirmation with the --force flag.

Examples:
    1. Remove all unused Docker resources:
       $ dev-cli docker-cleanup a

    2. Simulate removal of unused Docker resources:
       $ dev-cli docker-cleanup a --dry-run

    3. Force removal of stopped containers without confirmation:
       $ dev-cli docker-cleanup c --force

Notes:
    - `--dry-run` shows which resources would be deleted without actually removing them.
    - `--force` skips confirmation prompts and deletes resources automatically.
    - Use `--help` to get detailed information about any command or option.
"""

import click
import sys
from pathlib import Path
import docker
import logging

# =============== PATH SETUP

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# =============== LOGGING SETUP

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s.")
logger = logging.getLogger(__name__)

# =============== DOCKER CLIENT

def get_docker_client():
    """Returns a Docker client instance, handling errors properly."""
    try:
        return docker.from_env()
    except docker.errors.DockerException as e:
        logger.error(f"Failed to initialise Docker client: {e}")
        sys.exit(1)

# =============== CLI COMMANDS

def docker_connection_checker():
    """Check if Docker Daemon is running before executing any command."""
    client = get_docker_client()
    try:
        client.ping()
        return True
    except docker.errors.DockerException:
        logger.error("Docker daemon is not running or not accessible.")
        return False

# =============== CLICK GROUP

@click.group(help="""A CLI tool to clean up unused Docker resources.

Most commands support the [dry-run] flag to show what would be deleted
without actually deleting anything. Use --force to bypass confirmation.

Example: 'dev-cli docker-cleanup a --dry-run'""")
@click.option("--verbose", is_flag=True, help="Enable verbose output.")
@click.option("--log-level", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
              default="INFO", help="Set the logging level.")
def docker_cleanup(verbose, log_level):
    log_level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(log_level)
    if verbose:
        logger.debug("Verbose mode enabled.")

# =============== CLI COMMANDS

def prune_resource(resource_type, dry_run, force, filter_args=None):
    """Generalised function to prune Docker resources."""
    if not docker_connection_checker():
        return
    client = get_docker_client()
    try:
        prune_func = getattr(client, resource_type).prune
        if dry_run:
            logger.info(f"[dry-run] Would remove all unused {resource_type}.")
            # Log which resources would be affected in dry-run mode
            if resource_type == "containers":
                resources = client.containers.list(
                    all=True, filters=filter_args)
            elif resource_type == "images":
                resources = client.images.list(filters=filter_args)
            elif resource_type == "volumes":
                resources = client.volumes.list(filters=filter_args)
            elif resource_type == "networks":
                resources = client.networks.list(filters=filter_args)
            logger.info(
                f"[dry-run] {len(resources)} {resource_type} would be affected.")
        else:
            if not force and not click.confirm(f"Are you sure you want to remove all unused {resource_type}?"):
                return
            logger.info(f"Removing all unused {resource_type}.")
            prune_func(filters=filter_args)
            logger.info(f"All unused {resource_type} removed successfully.")

    except docker.errors.APIError as e:
        logger.error(f"Docker API error while pruning {resource_type}: {e}")
    except docker.errors.DockerException as e:
        logger.error(f"Docker exception while pruning {resource_type}: {e}")
    except Exception as e:
        logger.error(f"Error while pruning {resource_type}: {e}")


@click.command("c", help="Remove all stopped containers. Use --dry-run to preview.")
@click.option("--dry-run", is_flag=True, help="Simulate the command without making changes.")
@click.option("--force", is_flag=True, help="Skip confirmation prompts.")
def prune_containers(dry_run, force):
    prune_resource("containers", dry_run, force, {"status": "exited"})


@click.command("i", help="Remove all dangling images.")
@click.option("--dry-run", is_flag=True, help="Simulate the command without making changes.")
@click.option("--all", is_flag=True, help="Remove all unused images, not just dangling ones.")
@click.option("--force", is_flag=True, help="Skip confirmation prompts.")
def prune_images(dry_run, all, force):
    prune_resource("images", dry_run, force, {"dangling": not all})


@click.command("v", help="Remove all dangling volumes.")
@click.option("--dry-run", is_flag=True, help="Simulate the command without making changes.")
@click.option("--force", is_flag=True, help="Skip confirmation prompts.")
def prune_volumes(dry_run, force):
    prune_resource("volumes", dry_run, force)


@click.command("n", help="Remove all unused networks.")
@click.option("--dry-run", is_flag=True, help="Simulate the command without making changes.")
@click.option("--force", is_flag=True, help="Skip confirmation prompts.")
def prune_networks(dry_run, force):
    prune_resource("networks", dry_run, force)


@click.command("a", help="Remove all unused Docker resources.")
@click.option("--dry-run", is_flag=True, help="Simulate the command without making changes.")
@click.option("--force", is_flag=True, help="Skip confirmation prompts.")
def prune_all(dry_run, force):
    """Prune all unused containers, images, volumes, and networks."""
    if not docker_connection_checker():
        return
    client = get_docker_client()
    try:
        if dry_run:
            logger.info("[dry-run] Would remove all unused Docker resources.")
            # Log dry-run for all resources
            containers = client.containers.list(all=True)
            images = client.images.list()
            volumes = client.volumes.list()
            networks = client.networks.list()
            logger.info(f"[dry-run] {len(containers)} containers, {len(images)} images, {len(volumes)} volumes, "
                        f"{len(networks)} networks would be affected.")
        else:
            if not force and not click.confirm("Are you sure you want to remove all unused Docker resources?"):
                return
            logger.info("Removing all unused Docker resources.")
            client.containers.prune()
            client.images.prune()
            client.volumes.prune()
            client.networks.prune()
            logger.info("All unused Docker resources removed successfully.")
    except docker.errors.APIError as e:
        logger.error(f"Docker API error while pruning all resources: {e}")
    except docker.errors.DockerException as e:
        logger.error(f"Docker exception while pruning all resources: {e}")
    except Exception as e:
        logger.error(f"Error while pruning all resources: {e}")

# =============== ADDING COMMANDS TO GROUPS

docker_cleanup.add_command(prune_containers)
docker_cleanup.add_command(prune_images)
docker_cleanup.add_command(prune_volumes)
docker_cleanup.add_command(prune_networks)
docker_cleanup.add_command(prune_all)

# =============== SCRIPT ENTRYPOINT

if __name__ == "__main__":
    docker_cleanup()
