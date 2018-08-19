from os.path import join, dirname, exists

import pytest

from rs500common.configuration import ConfigProvider


def test_config_provider_smoke_error():
    with pytest.raises(FileNotFoundError):
        ConfigProvider('/does/not/exist.ini')


def test_config_provider_on_existing_file():
    file = join(dirname(__file__), '..', 'check_rs500.ini')
    assert exists(file)
    cf = ConfigProvider(file)
    keys = cf.get_config().keys()
    assert len(keys) > 0
