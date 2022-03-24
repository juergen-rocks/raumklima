from os.path import join, dirname, exists

from behave import *

from rs500common.configuration import ConfigProvider


@given("eine existierende Datei, z. B. '{file}'")
def existing_file(context, file):
    c_file = join(dirname(__file__), "..", "..", file)
    assert exists(c_file)
    context.file = c_file


@given("eine nicht-existierende Datei, z. B. '{file}'")
def non_existing_file(context, file):
    c_file = join(dirname(__file__), "..", "..", file)
    assert not exists(c_file)
    context.file = c_file


@when("das ConfigProvider-Objekt für die genannte Datei erzeugt wird")
def create_object(context):
    try:
        context.obj = ConfigProvider(context.file)
    except Exception as exc:
        context.exc = exc


@then("Objekt ist vom Typ ConfigProvider")
def object_type_config_provider(context):
    assert isinstance(context.obj, ConfigProvider)


@then("entsteht ein Objekt (es ist nicht None)")
def object_not_none(context):
    assert context.obj is not None


@then("enthält das Objekt Schlüssel")
def object_has_keys(context):
    assert len(context.obj.get_config().keys()) > 0


@then("wird eine Exception vom Typ 'FileNotFoundError' geworfen")
def exception_thrown(context):
    assert isinstance(context.exc, FileNotFoundError)
