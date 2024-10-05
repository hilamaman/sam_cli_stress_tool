from loguru import logger
import random
import yaml
import os

def get_domains_list(num_domains: int, domains_file: str) -> list:
    """
    Return a list of domains for testing.
    :param num_domains: The number of domains to return.
    :param domains_file: Path to the YAML file containing the list of domains.
    :return: A list of randomly chosen domains, with a maximum of 5000 domains.
    """
    logger.debug("Getting domains list")
    domains_list = [
        "google.com", "youtube.com", "facebook.com", "amazon.com", "wikipedia.org",
        "twitter.com", "instagram.com", "linkedin.com", "reddit.com", "netflix.com",
        "securingsam.com", "domaintest1.org", "domaintest2.co.il", "domaintest3.net",
        "domaintest4.gov", "."
    ]

    try:
        with open(domains_file, "r") as file:
            domains_list = yaml.safe_load(file)
            domains_list = domains_list["domains"]
            logger.info(f"Domain list loaded successfully from yaml file.")

    except FileNotFoundError:
        logger.error(f"Domain list file {domains_file} not found. using default list instead.")
    except Exception as e:
        logger.error(f"An unexpected error occurred while reading the file: {e}. using default list instead.")

    logger.debug('Successfully created domains list')
    return random.choices(domains_list, k=min(num_domains, 5000))

def get_api_token_env_var():
    """
    Return API_TOKEN environment variable as defined by user.
    :return: API_TOKEN as string if exists, None otherwise.
    """
    api_token = os.getenv('API_TOKEN')
    return api_token