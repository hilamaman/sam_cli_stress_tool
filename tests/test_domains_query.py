import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from argparse import Namespace
import requests

from cli_stress_tool.domains_query import DomainsQuery

@pytest.fixture
def mock_args():
    return Namespace(
        concurrent_requests=10,
        domains=500,
        timeout=60,
        log_level='INFO',
        api_url='https://example.com/api'
    )

@pytest.fixture
def mock_api_token():
    return 'mock_api_token'

@pytest.fixture
def mock_results_dir_path():
    return Path('/tmp/test_results')

@pytest.fixture
def domains_query(mock_args, mock_api_token, mock_results_dir_path):
    return DomainsQuery(mock_args, mock_api_token, mock_results_dir_path)

def test_init(domains_query, mock_args, mock_api_token, mock_results_dir_path):
    assert domains_query.args == mock_args
    assert domains_query.api_token == mock_api_token
    assert domains_query.results_dir_path == mock_results_dir_path

@patch('cli_stress_tool.domains_query.requests.get')
def test_query_domain_success(mock_get, domains_query):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'reputation': 'good'}
    mock_get.return_value = mock_response

    result = domains_query.query_domain('example.com')

    assert result['success'] == True
    assert result['status_code'] == 200
    assert result['reputation'] == 'good'

@patch('cli_stress_tool.domains_query.requests.get')
def test_query_domain_failure(mock_get, domains_query):
    mock_get.side_effect = requests.RequestException('Test error')

    result = domains_query.query_domain('example.com')

    assert result['success'] == False
    assert 'Test error' in result['error']
