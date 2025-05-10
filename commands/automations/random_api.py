
"""
isinstance() = built-in function used to check the type of a variable or object.
for exceptions: always place the most specific exceptions first, followed by more general ones.
    
    ValueError: specific exception
    Exception: catch-all block that will handle any other exceptions (should be at the end).

FREE API LINK:
https://apipheny.io/free-api/
"""

import click
import json
import sys
from pathlib import Path
import logging
from collections import defaultdict
import requests

# =============== PATH

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.insert(0, (parent_dir))

# =============== LOGGING

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s."
)
logger = logging.getLogger(__name__)

# =============== CLI GROUP

@click.group(help="A CLI tool for executing ramdom API calls.")
def random_api():
    """
    """
    pass

# =============== COMMANDS
# =============== CAT FACTS

@click.command(help="Run script to generate random cat facts.")
def cats():
    try:
        # send a GET request to get the CatFact API
        response = requests.get("https://catfact.ninja/fact")
        # will raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        # check if the response code is 200 (OK)
        if response.status_code == 200:
            # parse the response JSON
            response_json = response.json()

            # safely iterate over the key-value pairs in the JSON (if it's a dictionary)
            if isinstance(response_json, dict):
                # iterate over JSON data
                for k, v in response_json.items():
                    # log each key-value pair
                    logger.info(f"{k}: {v}")
            else:
                # warn if the response format is unexpected
                logger.warning("Unexpected response format.")
        else:
            # log an error if the status code is not 200 (OK)
            logger.error(f"Unable to get API response. Status code: {response.status_code}")

    # handle errors when the JSON is invalid (e.g., unable to parse)
    except ValueError as v:
        logger.error(f"Value error while parsing JSON: {v}")
    # catch all other unexpected exceptions.
    except Exception as e:
        logger.error(f"Exception occurred: {e}")

# =============== RANDOM ACTIVITIES

@click.command(help="Run script to generate random activities.")
def bored():
    try:
        # send a GET request to get the BoredPi API
        response = requests.get("https://www.boredapi.com/api/activity")
        # will raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        # check if the response code is 200 (OK)
        if response.status_code == 200:
            # parse over JSON data
            response_json = response.json()
            # safely iterate over the key-value pairs in the JSON (if it's a dictionary)
            if isinstance(response_json, dict):
                for k, v in response_json.items():
                    # log each key-value pair
                    logger.info(f"{k}: {v}")
            else:
                # warn if the response format is unexpected
                logger.error("Unexpected response format.")
        else:
            # log an error if the status code is not 200 (OK)
            logger.error(f"Unable to get API response. Status code: {response.status_code}")
    
    # handle errors when the JSON is invalid (e.g., unable to parse)
    except ValueError as v:
        logger.error(f"Value error whilst parsing JSON: {v}")
    # catch all other unexpected exceptions.
    except Exception as e:
        logger.error(f"Exception occured: {e}")

# =============== PREDICT GENDER

@click.command(help="Run script to predict gender based on name input.")
@click.option("-n", "--name", required=True, help="Input a random name.")
def gender(name):
    try:
        # send a GET request to get the Genderize API
        response = requests.get(f"https://api.genderize.io?name={name}")
        # will raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        # check if the response code is 200 (OK)
        if response.status_code == 200:
            # parse over the JSON data
            response_json = response.json()
            # safely iterate over the key-value pairs in the JSON (if it's a dictionary)
            if isinstance(response_json, dict):
                for k, v in response_json.items():
                    # log each key-value pair
                    logger.info(f"{k}: {v}")
            else:
                # warn if the response format is unexpected
                logger.error("Unexpected response format.")
        else:
            # warn if the status code is not 200 (OK)
            logger.error(f"Unable to get API response. Status code: {response.status_code}")
    # handle errors when the JSON is invalid (e.g./ unable to parse)
    except ValueError as v:
        logger.error(f"Value error whilst parsing JSON: {v}")
    # catch all other unexpected exceptions
    except Exception as e:
        logger.error(f"Exception occured: {e}")

# =============== PREDICT AGE

@click.command(help="Run script to predict age based on name input.")
@click.option("-n", "--name", required=True, help="Input a random name.")
def age(name):
    try:
        response = requests.get(f"https://api.agify.io?name={name}")
        # will raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        if response.status_code == 200:
            response_json = response.json()
            if isinstance(response_json, dict):
                for k, v in response_json.items():
                    logger.info(f"{k}: {v}")
            else:
                logger.error("Unexpected response format.")
        else:
            logger.error(f"Unable to get API response. Status code: {response.status_code}")
    except ValueError as v:
        logger.error(f"Value error whilst parsing JSON: {v}")
    except Exception as e:
        logger.error(f"Exception occured: {e}")

# =============== PREDICT NATIONALITY

@click.command(help="Run script to predict nationality based on name input")
@click.option("-n", "--name", required=True, help="Input a random name.")
def nationality(name):
    try:
        response = requests.get(f"https://api.nationalize.io?name={name}")
        response.raise_for_status()
        if response.status_code == 200:
            response_json = response.json()
            if isinstance(response_json, dict):
                countries = response_json.get("country", [])
                if countries:
                    logger.info(f"Results for the name '{name}':")
                    for country in countries:
                        country_name = country.get('country_id')
                        probability = country.get('probability') * 100  # Convert to percentage
                        logger.info(f"Country: {country_name.upper()} | Probability: {probability:.2f}%")
                else:
                    logger.warning(f"No country data found for the name '{name}'")
        else:
            logger.error(f"Unable to get API response. Status code: {response.status_code}")
    except ValueError as e:
        logger.error(f"Value error whilst parsing JSON: {e}")
    except Exception as e:
        logger.error(f"Exception occured: {e}")
    
# =============== ADD COMMANDS

random_api.add_command(cats)
random_api.add_command(bored)
random_api.add_command(gender)
random_api.add_command(age)
random_api.add_command(nationality)

if __name__ == "__main__":
    random_api()