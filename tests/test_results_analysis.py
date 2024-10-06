import pytest
from pathlib import Path
from cli_stress_tool.results_analysis import ResultsAnalysis


@pytest.fixture
def sample_results():
    return [
        {'success': True, 'duration': 0.1, 'domain': 'example1.com', 'status_code': 200, 'reputation': 'good'},
        {'success': True, 'duration': 0.2, 'domain': 'example2.com', 'status_code': 200, 'reputation': 'bad'},
        {'success': False, 'duration': 0.3, 'domain': 'example3.com', 'status_code': None, 'error': 'Timeout'},
    ]


@pytest.fixture
def results_analysis(sample_results):
    return ResultsAnalysis(sample_results, 1.0, Path('/tmp/test_results'))


def test_results_analysis(results_analysis):
    analysis = results_analysis.analysis
    assert analysis['total_request'] == 3
    assert analysis['successful_requests'] == 2
    assert analysis['failed_requests'] == 1
    assert analysis['timed_out_requests'] == 1
    assert analysis['error_rate'] == pytest.approx(1 / 3)
    assert analysis['min_request_dur'] == 0.1
    assert analysis['max_request_dur'] == 0.2
    assert analysis['avg_request_dur'] == pytest.approx(0.15)
    assert analysis['p90_request_dur'] == pytest.approx(0.19)


def test_print_results(results_analysis, capsys):
    results_analysis.print_results(1.0)
    captured = capsys.readouterr()
    assert "Test is over!" in captured.out
    assert "Reason: timeout" in captured.out
    assert "Time in total: 1.00 seconds" in captured.out
    assert "Requests in total: 3" in captured.out


@pytest.mark.parametrize("output_file", ["test_output.csv"])
def test_save_results_to_csv(results_analysis, output_file, tmp_path):
    results_analysis.results_dir_path = tmp_path
    results_analysis.save_results_to_csv(output_file)

    csv_files = list(tmp_path.glob(f"{output_file}_*.csv"))
    assert len(csv_files) == 1

    with open(csv_files[0], 'r') as f:
        content = f.read()
        assert 'Field,Value' in content
        assert 'Domain,Success,Time,Status code,Reputation,Info' in content
        assert 'example1.com,True,0.1,200,good,' in content
