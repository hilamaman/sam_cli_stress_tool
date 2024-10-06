import csv
import time
import numpy as np
from loguru import logger
from pathlib import Path


class ResultsAnalysis:
    def __init__(self, test_results: list, test_duration: float, results_dir_path: Path):
        self.results = test_results
        self.duration = test_duration
        self.analysis = self._results_analysis()
        self.results_dir_path = results_dir_path

    def _results_analysis(self) -> dict:
        """
        Analyze the test results and compute various statistics.
        :return: A dictionary containing analyzed results including total requests, successful requests,
                  failed requests, error rate, and various timing statistics.
        """
        logger.info('Analyzing test results...')
        total_requests = len(self.results)
        list_successful_requests = [r for r in self.results if r['success'] == True]
        successful_requests = len(list_successful_requests)
        timed_out_requests = sum(1 for r in self.results if r['status_code'] is None)
        failed_requests = total_requests - successful_requests
        error_rate = failed_requests / total_requests if total_requests > 0 else 0
        successful_requests_durations = [r['duration'] for r in list_successful_requests]
        min_request_dur = np.min(successful_requests_durations) if successful_requests_durations else 0
        max_request_dur = np.max(successful_requests_durations) if successful_requests_durations else 0
        avg_request_dur = np.mean(successful_requests_durations) if successful_requests_durations else 0
        p90_request_dur = np.percentile(successful_requests_durations, 90) if successful_requests_durations else 0

        logger.info('Analyzing test results completed')
        return {
            'total_request': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': failed_requests,
            'timed_out_requests': timed_out_requests,
            'error_rate': error_rate,
            'min_request_dur': min_request_dur,
            'max_request_dur': max_request_dur,
            'avg_request_dur': avg_request_dur,
            'p90_request_dur': p90_request_dur
        }

    def print_results(self, timeout: float) -> None:
        """
        Print a summary of the test results to the console.
        :param timeout: The timeout duration set for the stress test.
        """
        logger.info('Printing test results..')
        print("Test is over!")
        print("Reason: timeout" if self.duration >= timeout else "Reason: keyboard interrupt")
        print(f"Time in total: {self.duration:.2f} seconds")
        print(f"Requests in total: {self.analysis['total_request']}")
        print(f"Successful requests in total: {self.analysis['successful_requests']}")
        print(f"Failed requests in total: {self.analysis['failed_requests']}")
        print(f"Timed out requests in total: {self.analysis['timed_out_requests']}")
        print(f"Error rate: {self.analysis['error_rate']:.2%} ({self.analysis['failed_requests']}/ {self.analysis['total_request']})")
        print(f"Average time for one request: {self.analysis['avg_request_dur']*1000:.2f} ms")
        print(f"Max time for one request: {self.analysis['max_request_dur']:.2f} seconds")
        print(f"Min time for one request: {self.analysis['min_request_dur']:.2f} seconds")
        print(f"The 90th percentile time for one request: {self.analysis['p90_request_dur']:.2f} seconds")
        logger.info('Printing test results completed')

    def save_results_to_csv(self, output_file: str) -> None:
        """
        Save the test results and analysis to a CSV file.
        :param output_file: The name of the file to save the results to.
        """
        current_time = time.time()
        file_path = f"{output_file}_{current_time}.csv"
        logger.debug(f'Saving test results to csv at {file_path}')
        csv_output_path = self.results_dir_path / file_path
        with open(csv_output_path, mode='w', newline='') as file:
            summery_fieldnames = ['Field', 'Value']
            writer = csv.DictWriter(file, fieldnames=summery_fieldnames)
            writer.writeheader()
            for key, val in self.analysis.items():
                writer.writerow({
                    'Field': key,
                    'Value': val
                })

            results_fieldnames = ['Domain', 'Success', 'Time', 'Status code', 'Reputation', 'Info']
            writer = csv.DictWriter(file, fieldnames=results_fieldnames)
            writer.writeheader()
            for result in self.results:
                writer.writerow({
                    'Domain': result['domain'],
                    'Success': result['success'],
                    'Time': result['duration'],
                    'Status code': result.get('status_code', ''),
                    'Reputation': result.get('reputation', '') if result.get('reputation') is not None else 0,
                    'Info': result.get('data', '') if result.get('data') else result.get('error', '')
                })
        logger.info(f"Saving test results to csv completed")