import pytest
from src.core.config import ConfigManager


def test_config_load_default():
    config = ConfigManager(config_path='config/lucille.conf')
    assert config.get('framework.name') == 'Lucille'
    assert config.get('modules.enabled')


def test_config_set_get():
    config = ConfigManager(config_path='config/lucille.conf')
    config.set('framework.parallel_threads', 5)
    assert config.get('framework.parallel_threads') == 5
