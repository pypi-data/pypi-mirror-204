import os
import tempfile
import pytest
import yaml

from YamlStripper.yaml_stripper import remove_fields


@pytest.fixture
def test_yaml():
    return {
        "name": "Test YAML",
        "description": "This is a test YAML file",
        "author": "John Doe",
        "version": "1.0.0",
        "fields": [
            {"name": "field1", "type": "string", "required": True},
            {"name": "field2", "type": "integer", "required": False},
            {"name": "field3", "type": "boolean", "required": True}
        ]
    }


def test_remove_fields(test_yaml):
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        yaml_file = tmp.name
        yaml.dump(test_yaml, tmp)

    new_yaml_file = os.path.join(tempfile.gettempdir(), "new_test_yaml.yml")

    # remove 'name' and 'description' fields
    remove_fields(yaml_file, ["name", "description"], new_yaml_file)

    with open(new_yaml_file, "r") as f:
        data = yaml.safe_load(f)

    # assert that 'name' and 'description' fields were removed
    assert "name" not in data
    assert "description" not in data

    # assert that other fields are still present
    assert "author" in data
    assert "version" in data
    assert "fields" in data

    # cleanup
    os.remove(yaml_file)
    os.remove(new_yaml_file)
