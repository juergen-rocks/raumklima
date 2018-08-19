import os.path

import pytest
from _pytest.monkeypatch import MonkeyPatch

from rs500common.configuration import discover_config_file_by_name


def test_discovery(monkeypatch: MonkeyPatch):
    with monkeypatch.context() as m:
        m.setattr('os.path.isfile', lambda path: True)
        m.setattr('os.path.exists', lambda path: True)
        result = discover_config_file_by_name('test.ini', '/foo/bar')
    assert result == os.path.join('/foo/bar', 'test.ini')


def test_no_hit():
    with pytest.raises(FileNotFoundError):
        discover_config_file_by_name('does-not-exist.nothing', 'bla-blubb')
