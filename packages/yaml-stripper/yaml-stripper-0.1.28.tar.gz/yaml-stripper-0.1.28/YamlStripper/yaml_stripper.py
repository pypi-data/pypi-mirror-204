import argparse
import ruamel.yaml


def remove_fields(yaml_file, fields_to_remove, new_yaml_file):
    """Remove specified fields from a YAML file while maintaining the order of fields.

    Args:
        yaml_file (str): The input YAML file.
        fields_to_remove (list): The fields to remove.
        new_yaml_file (str): The output YAML file without the specified fields.

    """

    with open(yaml_file, 'r') as f:
        yaml = ruamel.yaml.YAML()
        data = yaml.load(f)

    for field in fields_to_remove:
        # strip whitespace from beginning and end of field name
        field = field.strip()
        if field not in data:
            print(f"Field '{field}' not found in YAML file")
        else:
            # remove field and any indented child fields
            field_keys = field.split('.')
            while len(field_keys) > 0:
                key = field_keys.pop(0)
                if key not in data:
                    print(f"Field '{field}' not found in YAML file")
                    break
                elif len(field_keys) == 0:
                    del data[key]
                else:
                    data = data[key]

    with open(new_yaml_file, 'w') as f:
        yaml.dump(data, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Remove specified fields from a YAML file while maintaining the order of fields.')

    parser.add_argument('yaml_file', type=str, help='The input YAML file')
    parser.add_argument('new_yaml_file', type=str,
                        help='The output YAML file without the specified fields')
    parser.add_argument('-f', '--fields', type=str, nargs='+',
                        help='The fields to remove', required=True)

    args = parser.parse_args()

    remove_fields(args.yaml_file, args.fields, args.new_yaml_file)
