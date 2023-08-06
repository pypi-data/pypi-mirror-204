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
        if field in data:
            del data[field]

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
