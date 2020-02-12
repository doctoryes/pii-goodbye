"""
Second stage in generating Pii redactions.

Parses the output of parse_ann_report.py which has been augmented manually with
data about class/table names and fields to redact. Generates YML to add/merge to
the redactions.yml file in the warehouse-transforms repo.
"""

import click
import yaml

def parse_pii_data(infile):
    pii_redactions = {}
    with open(infile, 'r') as pii_file:
        pii_data = yaml.load(pii_file, Loader=yaml.FullLoader)
    for filename in pii_data:
        for model in pii_data[filename]:
            table_name = model['db_table_name']
            pii_fields = model['pii_fields']
            schema_table = '{app_name}.{table_name}'.format(app_name='LMS', table_name=table_name.upper())
            redactions = {}
            for field, val in pii_fields.items():
                if isinstance(val, str):
                    val = "'{}'".format(val)
                redactions[field.upper()] = val
            pii_redactions[schema_table] = redactions
    return pii_redactions

def generate_redaction_yml(pii_data, outfile):
    with open(outfile, 'w') as redactions_file:
        yaml.dump(pii_data, redactions_file)


@click.command()
@click.option('--infile',
              default='pii_models.txt',
              help="YAML file - the output of parse_ann_report.py - plus manual additions.",
              required=False
              )
@click.option('--outfile',
              default='redactions.yml',
              help="YAML to add to the warehouse-transforms redactions.yml file.",
              required=False
              )
def cli(infile, outfile):
    """
    Parses the output of parse_ann_report.py which has been augmented manually with
    data about class/table names and fields to redact. Generates YML to add/merge to
    the redactions.yml file in the warehouse-transforms repo.
    """
    pii_annotation_data = parse_pii_data(infile)
    generate_redaction_yml(pii_annotation_data, outfile)

if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter