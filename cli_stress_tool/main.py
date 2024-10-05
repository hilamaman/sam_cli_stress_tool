import argparse
from cli_stress_tool.utils import get_api_token_env_var
from cli_stress_tool.domains_query import DomainsQuery
from cli_stress_tool.results_analysis import ResultsAnalysis
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--concurrent_requests', default=10, type=int)
    parser.add_argument('--domains', default=500, type=int)
    parser.add_argument('--timeout', default=60, type=int)
    parser.add_argument('--results_file_path', type=str, default='stress_test_results')
    parser.add_argument('--domains_file_path', type=str, default='./assets/domains.yaml')
    parser.add_argument('--log_level', type=str, default='INFO')
    parser.add_argument('--api_url', type=str,
                        default='https://microcks.gin.dev.securingsam.io/rest/Reputation+API/1.0.0/domain/ranking')
    args = parser.parse_args()


    api_token = get_api_token_env_var()
    if api_token is None:
        parser.error('Please provide an API token as environment variable (How-To can be found in README).')
    if args.domains > 5000:
        parser.error(f"Number of domains cannot exceed 5000.")
    if args.concurrent_requests < 1:
        parser.error("Number of concurrent requests cannot be less than 1.")
    if args.timeout < 1:
        parser.error("Timeout cannot be less than 1.")

    results_dir_path = Path().cwd() / "results"

    domains_query = DomainsQuery(args, api_token, results_dir_path)
    results, duration = domains_query.stress_test()

    results_analyzer = ResultsAnalysis(results, duration, results_dir_path)
    results_analyzer.print_results(args.timeout)
    results_analyzer.save_results_to_csv(args.results_file_path)

if __name__ == '__main__':
    main()