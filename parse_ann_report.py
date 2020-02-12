"""
First stage in generating PII redactions.

Parses an application's PII annotations and outputs YAML with enhanced versions
of each annotation indicating PII is present. The output YAML is ready to be
manually augmented with the db_table_name and pii_fields.
"""

import click
from yaml import load, dump

NO_PII_ANNOTATION = '.. no_pii:'
PII_TYPES_ANNOTATION = '.. pii_types:'
GH_URL_FORMAT = 'https://github.com/edx/edx-platform/blob/master/{filename}#L{line_number}'

def parse_pii_data(infile):
    pii_models = {}
    with open(infile, 'r') as pii_file:
        pii_data = load(pii_file)
    for filename in pii_data:
        for annotation in pii_data[filename]:
            if NO_PII_ANNOTATION in annotation['annotation_token']:
                continue
            elif PII_TYPES_ANNOTATION in annotation['annotation_token']:
                annotation['github_url'] = GH_URL_FORMAT.format(
                    filename = annotation['filename'],
                    line_number = annotation['line_number']
                )
                annotation['python_class'] = None
                annotation['db_table_name'] = None
                annotation['pii_fields'] = []
                if filename in pii_models:
                    pii_models[filename].append(annotation)
                else:
                    pii_models[filename] = [annotation]
    return pii_models

def generate_report(pii_data, outfile):
    with open(outfile, 'w') as pii_outfile:
        dump(pii_data, pii_outfile)

@click.command()
@click.option('--infile',
              default='edxapp_pii_report.yaml',
              help="YAML file - the output of the PII annotation report.",
              required=False
              )
@click.option('--outfile',
              default='pii_models.yml',
              help="YAML file containing output of views/fields to redact.",
              required=False
              )
def cli(infile, outfile):
    """
    Parses an application's PII annotations and outputs YAML with enhanced versions
    of each annotation indicating PII is present.
    """
    pii_annotation_data = parse_pii_data(infile)
    generate_report(pii_annotation_data, outfile)

if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter