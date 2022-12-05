import pytest
import os


def pytest_collection_modifyitems(items):
    for item in items:
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.slow)
            item.add_marker(pytest.mark.integration)


def pytest_generate_tests(metafunc):
    if metafunc.definition.name == "test_each_module":
        metafunc.parametrize("module", [
                x.name for x in os.scandir(
                    metafunc.definition.config.rootdir / "src/disaggregators/disaggregation_modules"
                ) if x.is_dir() and not x.name.startswith("__")
        ])
