import os
from src.core.engine import LucilleEngine


def test_engine_scan_mock_target(tmp_path):
    engine = LucilleEngine()
    engine.results_dir = tmp_path
    result = engine.scan('example.com', modules='quick', parallel=2, timeout=10)

    assert result['status'] == 'completed'
    assert 'port_scan' in result['modules']
    assert 'web_scan' in result['modules']
    assert (tmp_path / 'example.com' / 'latest.json').exists()
