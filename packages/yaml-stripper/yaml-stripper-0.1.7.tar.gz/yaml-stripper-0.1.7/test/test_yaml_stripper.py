import io
import yaml
import pytest
import yaml_stripper


def test_load_yaml():
    yaml_str = "foo: bar\nbaz: qux\n"
    yaml_file = io.StringIO(yaml_str)
    expected_yaml = {"foo": "bar", "baz": "qux"}

    yaml_data = yaml_stripper.load_yaml(yaml_file)

    assert yaml_data == expected_yaml


def test_dump_yaml():
    yaml_data = {"foo": "bar", "baz": "qux"}
    expected_yaml_str = "foo: bar\nbaz: qux\n"
    yaml_file = io.StringIO()

    yaml_stripper.dump_yaml(yaml_data, yaml_file)

    yaml_file.seek(0)
    assert yaml_file.read() == expected_yaml_str


def test_strip_fields():
    yaml_data = {"foo": "bar", "baz": "qux", "quux": "corge"}
    fields_to_remove = ["baz", "quux"]
    expected_yaml = {"foo": "bar"}

    stripped_yaml = yaml_stripper.strip_fields(yaml_data, fields_to_remove)

    assert stripped_yaml == expected_yaml


def test_main_success():
    input_yaml_str = "foo: bar\nbaz: qux\nquux: corge\n"
    expected_output_yaml_str = "foo: bar\n"
    input_yaml_file = io.StringIO(input_yaml_str)
    output_yaml_file = io.StringIO()
    fields_to_remove = ["baz", "quux"]

    yaml_stripper.main(input_yaml_file, output_yaml_file, fields_to_remove)

    output_yaml_file.seek(0)
    output_yaml_data = yaml.safe_load(output_yaml_file)
    expected_output_yaml_data = yaml.safe_load(expected_output_yaml_str)

    assert output_yaml_data == expected_output_yaml_data


def test_main_failure():
    input_yaml_str = "foo: bar\nbaz: qux\nquux: corge\n"
    input_yaml_file = io.StringIO(input_yaml_str)
    output_yaml_file = io.StringIO()
    fields_to_remove = ["quuz"]

    with pytest.raises(ValueError):
        yaml_stripper.main(input_yaml_file, output_yaml_file, fields_to_remove)
