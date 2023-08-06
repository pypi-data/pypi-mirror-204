import os
import tempfile
import yaml
import pytest

from YamlStripper.yaml_stripper import remove_fields


@pytest.fixture
def input_yaml():
    # create temporary input YAML file for testing
    data = {
        'name': 'John Doe',
        'age': 30,
        'address': {
            'street': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip': '12345'
        },
        'phone_numbers': [
            {
                'type': 'home',
                'number': '555-1234'
            },
            {
                'type': 'work',
                'number': '555-5678'
            }
        ]
    }
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        yaml.dump(data, f)
    yield f.name
    os.remove(f.name)


def test_remove_fields(input_yaml):
    # create temporary output YAML file for testing
    output_yaml = tempfile.NamedTemporaryFile(mode='w', delete=False).name

    # remove 'address.zip' and 'phone_numbers.type' fields
    fields_to_remove = ['address.zip', 'phone_numbers.type']
    remove_fields(input_yaml, fields_to_remove, output_yaml)

    # load output YAML file and check that fields were removed
    with open(output_yaml, 'r') as f:
        output_data = yaml.safe_load(f)

    assert 'zip' not in output_data['address']
    assert 'type' not in output_data['phone_numbers'][0]
    assert 'type' not in output_data['phone_numbers'][1]

    # remove 'phone_numbers' field
    fields_to_remove = ['phone_numbers']
    remove_fields(input_yaml, fields_to_remove, output_yaml)

    # load output YAML file and check that field was removed
    with open(output_yaml, 'r') as f:
        output_data = yaml.safe_load(f)

    assert 'phone_numbers' not in output_data

    os.remove(output_yaml)
