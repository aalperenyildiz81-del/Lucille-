from src.core.module_manager import ModuleManager


def test_module_loading():
    manager = ModuleManager()
    modules = manager.get_all_modules()
    assert 'port_scan' in modules
    assert 'web_scan' in modules


def test_module_info_detailed():
    manager = ModuleManager()
    info = manager.get_all_modules_detailed()
    assert 'port_scan' in info
    assert info['port_scan']['description'] != ''
