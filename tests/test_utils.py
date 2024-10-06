from unittest.mock import patch, mock_open
from cli_stress_tool.utils import get_domains_list, get_api_token_env_var

def test_get_domains_list_default():
    domains = get_domains_list(5, 'nonexistent_file.yaml')
    assert len(domains) == 5
    assert all(isinstance(domain, str) for domain in domains)

@patch('yaml.safe_load')
def test_get_domains_list_from_file(mock_yaml_load):
    mock_yaml_load.return_value = {'domains': ['domain1.com', 'domain2.com', 'domain3.com']}
    mock_file = mock_open()
    with patch('builtins.open', mock_file):
        domains = get_domains_list(2, 'test_domains.yaml')
    assert len(domains) == 2
    assert all(domain in ['domain1.com', 'domain2.com', 'domain3.com'] for domain in domains)

def test_get_domains_list_max_limit():
    domains = get_domains_list(6000, 'nonexistent_file.yaml')
    assert len(domains) == 5000

@patch.dict('os.environ', {'API_TOKEN': 'test_token'})
def test_get_api_token_env_var():
    token = get_api_token_env_var()
    assert token == 'test_token'

@patch.dict('os.environ', {}, clear=True)
def test_get_api_token_env_var_not_set():
    token = get_api_token_env_var()
    assert token is None
