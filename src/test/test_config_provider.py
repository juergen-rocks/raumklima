from os.path import join, dirname

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from rs500common.configuration import ConfigProvider


scenarios(join(dirname(__file__), "features", "config-provider.feature"))


@pytest.fixture(scope="function")
def filename():
    return ""


@pytest.fixture(scope="function")
def config_provider_object():
    return None


@pytest.fixture(scope="function")
def exception():
    return None


@given(parsers.parse("eine existierende Datei, z. B. '{file}'"), target_fixture="filename")
def existing_file(file):
    return file


@given(parsers.parse("eine nicht-existierende Datei, z. B. '{file}'"), target_fixture="filename")
def non_existing_file(file):
    return file


@when("das ConfigProvider-Objekt für die genannte Datei erzeugt wird", target_fixture="config_provider_object")
def create_object(filename):
    file = join(dirname(__file__), "..", filename)
    try:
        return ConfigProvider(file)
    except Exception as exc:
        return exc


@then("Objekt ist vom Typ ConfigProvider")
def object_type_config_provider(config_provider_object):
    assert isinstance(config_provider_object, ConfigProvider)


@then("entsteht ein Objekt (es ist nicht None)")
def object_not_none(config_provider_object):
    assert config_provider_object is not None


@then("enthält das Objekt Schlüssel")
def object_has_keys(config_provider_object):
    assert len(config_provider_object.get_config().keys()) > 0


@then("wird eine Exception vom Typ 'FileNotFoundError' geworfen")
def exception_thrown(config_provider_object):
    assert isinstance(config_provider_object, FileNotFoundError)
