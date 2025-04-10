
# ========== IMPORT LIBRARIES

import click
import json
import logging
import sys
import datetime
from pathlib import Path

# ========== PATH CONFIG

current_dir =  Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# ========== LOGGING CONFIG

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s.")
logger = logging.getLogger(__name__)

# ========== CACHE GROUP

@click.group(help="A CLI tool to securely manage credentials, tokens, and API keys in an encrypted cache.")
def cache():
    pass

# =============== CACHE CLI COMMANDS

@click.command(help="Add credentials to your cache securely.")
@click.option("-k", "--key", required=True, type=str, help="Add credentials in your cache against a key.")
def add_credential():
    pass

# ========== ADD COMMANDS TO CACHE GROUP

cache.add_command(add_credential)

# ========== MAIN ENTRYPOINT

if __name__ == "__main":
    cache()