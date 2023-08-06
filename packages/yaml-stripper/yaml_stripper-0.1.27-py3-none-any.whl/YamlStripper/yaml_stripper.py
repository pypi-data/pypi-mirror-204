import argparse
import yaml


def remove_fields(yaml_file, fields_to_remove, new_yaml_file):
    """Remove specified fields from a YAML file.

    Args:
        yaml_file (str): The input YAML file.
        fields_to_remove (list): The fields to remove.
        new_yaml_file (str): The output YAML file without the specified fields.

    """

    with open(yaml_file, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    for field in fields_to_remove:
        # strip whitespace from beginning and end of field name
        field = field.strip()

        if '.' in field:
            # if field contains nested keys, remove the nested field
            keys = field.split('.')
            sub_data = data
            for key in keys[:-1]:
                sub_data = sub_data.get(key, None)
                if sub_data is None:
                    break
            if sub_data is not None:
                sub_data.pop(keys[-1], None)
        else:
            # remove top-level field
            data.pop(field, None)

    with open(new_yaml_file, 'w') as f:
        yaml.dump(data, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Remove specified fields from a YAML file')

    parser.add_argument('yaml_file', type=str, help='The input YAML file')
    parser.add_argument('new_yaml_file', type=str,
                        help='The output YAML file without the specified fields')
    parser.add_argument('-f', '--fields', type=str, nargs='+',
                        help='The fields to remove', required=True)

    args = parser.parse_args()

    remove_fields(args.yaml_file, args.fields, args.new_yaml_file)
