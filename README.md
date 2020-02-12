# pii-goodbye

## Steps
- Generate PII annotation YAML report within a repo with annotations.
- Run the `parse_ann_report.py` script with the above report as input.
    - The output report is meant to be augmented by manual research.
- Use the generated URLs within the above output to examine the source code.
    - Fill in the following information manually for each model:
        - `python_class`
        - `db_table_name`
        - `pii_fields`
- Run the `output_view_redactions.py` script with the above manually-augmented file as input.
- Merge the output YAML with the existing [redactions file](https://github.com/edx/warehouse-transforms/blob/master/app_views_project/redactions.yml).

## TODO
- Accept `redactions.yml` as input for merging into any newly found redactions.
