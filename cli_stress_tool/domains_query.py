import itertools
import sys
import time
from argparse import Namespace
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import requests
from cli_stress_tool.utils import get_domains_list
from loguru import logger
from pathlib import Path

class DomainsQuery:
    def __init__(self, args: Namespace, api_token: str, results_dir_path: Path):
        self.args = args
        self.api_token = api_token
        self.results_dir_path = results_dir_path
        self._setup_logging()

    def _setup_logging(self) -> None:
        """
        Set up logging for the Domain Query.
        This method configures logging to both a file and stderr based on the specified log level.
        """
        logger.remove()
        current_time = time.time()
        logger.add(self.results_dir_path / f"logger_{current_time}.log", level=self.args.log_level.upper())
        logger.add(sys.stderr, level='ERROR')

        logger.info("Initialized Domain Query with cli args")

    def query_domain(self, domain: str) -> dict:
        """
        Query a single domain and return the result.
        :param domain: The domain to query.
        :return: A dictionary containing the query result
        """
        start_time = time.time()
        url = self.args.api_url + '/' + domain
        headers = {"Authorization": self.api_token}

        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            logger.debug(f"Query domain {domain} done successfully")
            return {
                'domain': domain,
                'success': True,
                'duration': time.time() - start_time,
                'status_code': response.status_code,
                'reputation': response.json()['reputation'],
                'data': response.json()
            }
        except requests.Timeout:
            logger.error(f"Query domain {domain} failed as result of time out")
            return {
                'domain': domain,
                'success': False,
                'duration': time.time() - start_time,
                'status_code': None,
                'error': 'Request timed out'
            }
        except requests.RequestException as e:
            logger.error(f"Query domain {domain} failed. error: {e}")
            return {
                'domain': domain,
                'success': False,
                'duration': time.time() - start_time,
                'status_code': e.response.status_code if e.response else None,
                'error': str(e)
            }

    def stress_test(self) -> tuple:
        """
        Perform a stress test by querying multiple domains concurrently.
        This method runs queries on domains in a loop until the specified timeout is reached or the test is interrupted.
        :return: A tuple containing a list of results and the total duration of the test.
        """
        logger.info(f"Starting stress test with {self.args.concurrent_requests} concurrent requests, "
                    f"{self.args.domains} domains and {self.args.timeout}s timeout.")

        results = []
        domains_list = get_domains_list(self.args.domains, self.args.domains_file_path)
        start_time = time.time()
        end_time = start_time + self.args.timeout

        with ThreadPoolExecutor(max_workers=self.args.concurrent_requests) as executor:
            domain_cycle = itertools.cycle(domains_list)
            futures = set()
            try:
                while time.time() < end_time:
                    while len(futures) < self.args.concurrent_requests and time.time() < end_time:
                        domain = next(domain_cycle)
                        future = executor.submit(self.query_domain, domain)
                        futures.add(future)

                    done, not_done = wait(futures, timeout=1, return_when=FIRST_COMPLETED)

                    for future in done:
                        results.append(future.result())
                        futures.remove(future)

                    if time.time() >= end_time:
                        break

            except KeyboardInterrupt:
                logger.error('Test stopped due to keyboard interrupt')
            finally:
                for future in futures:
                    future.cancel()
                executor.shutdown(wait=True)

        duration = time.time() - start_time
        logger.info(f'Stress test completed in {duration} seconds')
        return results, duration
