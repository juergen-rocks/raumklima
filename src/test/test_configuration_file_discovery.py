import os

import pytest
from _pytest.monkeypatch import MonkeyPatch

from rs500common.configuration import discover_config_file_by_name


def test_discovery(monkeypatch: MonkeyPatch):
    def mock(path):
        return True
    with monkeypatch.context() as m:
        m.setattr(os.path, 'isfile', mock)
        m.setattr(os.path, 'exists', mock)
        result = discover_config_file_by_name('test.ini', '/foo/bar')
    assert result == os.path.join('/foo/bar', 'test.ini')


def test_no_hit():
    with pytest.raises(FileNotFoundError):
        discover_config_file_by_name('does-not-exist.nothing', 'bla-blubb')
