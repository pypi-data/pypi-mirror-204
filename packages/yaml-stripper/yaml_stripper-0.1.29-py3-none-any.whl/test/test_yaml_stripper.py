import yaml
import io


def test_remove_field():
    # define the YAML string
    yaml_str = '''
    database:
      host: localhost
      port: 3306
      name: my_database
      credentials:
        user: my_username
        password: my_password
    '''
    # load the YAML data into a dictionary
    data = yaml.load(yaml_str, Loader=yaml.FullLoader)

    # remove the 'credentials' field from the dictionary
    remove_field(data, 'credentials')

    # define the expected result as a YAML string
    expected_yaml_str = '''
    database:
      host: localhost
      port: 3306
      name: my_database
    '''

    # load the expected YAML data into a dictionary
    expected_data = yaml.load(expected_yaml_str, Loader=yaml.FullLoader)

    # assert that the actual result matches the expected result
    assert data == expected_data

    # write the actual result to a YAML string
    actual_yaml_str = yaml.dump(data)

    # assert that the actual YAML string matches the expected YAML string
    assert actual_yaml_str == expected_yaml_str
