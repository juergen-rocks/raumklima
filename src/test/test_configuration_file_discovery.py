import os.path
import pathlib

import pytest
from _pytest.monkeypatch import MonkeyPatch

from rs500common.configuration import discover_config_file_by_name


def test_discovery_file_in_folder(monkeypatch: MonkeyPatch):
    with monkeypatch.context() as m:  # type: MonkeyPatch
        m.setattr('os.path.isfile', lambda path: True)
        m.setattr('os.path.exists', lambda path: True)
        result = discover_config_file_by_name('test.ini', '/foo/bar')
    assert os.path.join('/foo/bar', 'test.ini') == result


def test_discovery_via_env_var(monkeypatch: MonkeyPatch):
    with monkeypatch.context() as m:  # type: MonkeyPatch
        m.setenv('RS500_CONFIG_PATH', '/rs500_config_path/here/we/are')
        m.setattr('os.path.isfile', lambda path: True)
        m.setattr('os.path.exists', lambda path: True)
        result = discover_config_file_by_name('test.ini', script_dir=None)
    assert os.path.join('/rs500_config_path/here/we/are', 'test.ini') == result


def test_discovery_via_user_home(monkeypatch: MonkeyPatch):
    with monkeypatch.context() as m:  # type: MonkeyPatch
        m.setattr('os.path.isfile', lambda path: True)
        m.setattr('os.path.exists', lambda path: True)
        monkeypatch.setattr(pathlib.Path, 'absolute', lambda x: '/user/home/path/test')
        result = discover_config_file_by_name('test.ini', script_dir=None)
    assert os.path.join('/user/home/path/test', '.rs500', 'test.ini') == result


def test_discovery_in_etc(monkeypatch: MonkeyPatch):
    with monkeypatch.context() as m:  # type: MonkeyPatch
        m.setattr('os.path.isfile', lambda path: path.startswith('/etc'))
        m.setattr('os.path.exists', lambda path: path.startswith('/etc'))
        result = discover_config_file_by_name('test.ini')
    assert os.path.join('/etc', 'test.ini') == result


def test_no_hit():
    with pytest.raises(FileNotFoundError):
        discover_config_file_by_name('does-not-exist.nothing', 'bla-blubb')
