# Reputation Service Stress Test Tool

This CLI tool is designed to simulate stress on a Reputation service by sending multiple concurrent requests to the server. It allows you to test the performance and reliability of the service under various load conditions.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Configuration](#configuration)
4. [How It Works](#how-it-works)
5. [Output](#output)
6. [Examples](#examples)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/hilamaman/sam_cli_stress_tool.git
   cd sam_cli_stress_tool
   ```

2. Set Environment Variable for API_TOKEN
   - On Linux/macOS: 
   ```
   export API_TOKEN='your_api_token'
   ```
   
   - On Windows (Command Prompt)
   ```
   set API_TOKEN=your_api_token
   ```
   - On Windows (PowerShell)
   ```
   $env:API_TOKEN = "your_api_token"
   ```

3. From the root directory of the project (where `setup.py` is located), run:

   ```
   pip install .
   ```

   This will install the `cli_stress_tool` package and its dependencies.


### Usage

The installation creates a `cli_stress_tool` command that you can run from anywhere in your terminal:

```
cli_stress_tool [options]
```

### Options:

- `--concurrent_requests`: Number of concurrent requests (threads to run in parallel). Default: 10.
- `--domains`: Number of different domains to test (max: 5000). Default: 500.
- `--timeout`: Time in seconds to run the stress test. Default: 60.
- `--results_file_path`: Path to save the CSV results. Default: 'stress_test_results'
- `--domains_file_path`: Path to the YAML file containing the list of domains. Default: './assets/domains.yaml'.
- `--log_level`: Logging level. Default: 'INFO'.
- `--api_url`: API URL for the Reputation service. Default: 'https://microcks.gin.dev.securingsam.io/rest/Reputation+API/1.0.0/domain/ranking'.

## Configuration

Prepare a YAML file (`domains.yaml`) with a list of domains to test. The file should have the following structure:

   ```yaml
   domains:
     - google.com
     - youtube.com
     - facebook.com
     # Add more domains...
   ```


## How It Works

1. The tool reads the list of domains from the specified YAML file.
2. It creates a thread pool with the specified number of concurrent requests.
3. Domains are cycled through and queried until the timeout is reached or all domains have been tested.
4. Results are collected for each query, including success status, duration, and response data.
5. If a keyboard interrupt occurs, the test gracefully terminates and reports results up to that point.
6. After completion, the tool analyzes the results and prints a summary to the console.
7. Detailed results are saved to a CSV file for further analysis.

## Output

The tool provides two types of output:

1. Console output:
   - Test completion reason (timeout or keyboard interrupt)
   - Total time taken
   - Total number of requests
   - Error rate (number and percentage)
   - Average, max, and 90th percentile request times

2. CSV file output:
   - Summary statistics
   - Detailed results for each query

## Examples

1. Run a stress test with 20 concurrent requests, 1000 domains, and a 2-minute timeout:

   ```
   cli_stress_tool --concurrent_requests 20 --domains 1000 --timeout 120
   ```

2. Run a test with custom file paths and increased log level:

   ```
   cli_stress_tool --concurrent_requests 50 --domains 2000 --timeout 300 --results_file_path custom_results --domains_file_path custom_domains.yaml --log_level DEBUG
   ```

3. Run a quick test with default settings:

   ```
   cli_stress_tool
   ```

## Notes

- The tool is designed to handle various edge cases, including API failures and timeouts.
- It will not exceed the maximum of 5000 domains, even if a larger number is specified.
- The test will continue cycling through domains if the timeout hasn't been reached, even if all domains have been tested once.
- Results are continuously updated, allowing for meaningful output even if the test is interrupted.

For any issues or feature requests, please open an issue on the GitHub repository.