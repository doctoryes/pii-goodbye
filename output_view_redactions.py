"""
Second stage in generating Pii redactions.

Parses the output of parse_ann_report.py which has been augmented manually with
data about class/table names and fields to redact. Generates YML to add/merge to
the redactions.yml file in the warehouse-transforms repo.
"""

import click
from yaml import load, dump

def parse_pii_data(infile):
    pii_redactions = {}
    with open(infile, 'r') as pii_file:
        pii_data = load(pii_file)
    for filename in pii_data:
        for model in pii_data[filename]:
            table_name = model['db_table_name']
            pii_fields = model['pii_fields']
            schema_table = '{app_name}.{table_name}'.format(app_name='LMS', table_name=table_name)
            pii_redactions[schema_table] = [pii_fields]
    return pii_redactions

def generate_redaction_yml(pii_data, outfile):
    with open(outfile, 'w') as redactions_file:
        dump(pii_data, redactions_file)


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