import click
from YamlStripper.yaml_stripper import remove_fields


@click.command()
@click.argument("input_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
@click.option(
    "--fields", "-f", multiple=True, help="Fields to remove from the YAML file."
)
def main(input_file, output_file, fields):
    """
    Strip specified fields from a YAML file.

    INPUT_FILE: The YAML file to read.
    OUTPUT_FILE: The file to write the stripped YAML to.
    FIELDS: Fields to remove from the YAML file.
    """
    # Load the input YAML file
    yaml_data = yaml_stripper.load_yaml(input_file)

    # Remove specified fields from the YAML data
    stripped_yaml = yaml_stripper.strip_fields(yaml_data, fields)

    # Write the stripped YAML to the output file
    yaml_stripper.dump_yaml(stripped_yaml, output_file)


if __name__ == "__main__":
    main()
