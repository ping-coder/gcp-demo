from google.cloud import bigquery

def create(
    project_id: str = "your-project-id",
    dataset_id: str = "your-dataset-id",
    table_id: str = "your-table-id",
    schema_fields: tuple = None,
):
    # Create a client
    client = bigquery.Client()

    table = bigquery.Table(
        table_ref=bigquery.TableReference(bigquery.DatasetReference(project=project_id, dataset_id=dataset_id), table_id=table_id),
        schema=schema_fields
    )

    table = client.create_table(table=table, exists_ok=True)  # API request
    print(f"[table_client] Created {table_id}.")

    # View table properties
    print(
        "Got table '{}.{}.{}'.".format(table.project, table.dataset_id, table.table_id)
    )
    print("Table schema: {}".format(table.schema))
    print("Table description: {}".format(table.description))
    print("Table has {} rows".format(table.num_rows))
    return table

id_field = bigquery.SchemaField(name="id", field_type="STRING", mode="REQUIRED")
name_field = bigquery.SchemaField(name="email", field_type="STRING", mode="REQUIRED", policy_tags=bigquery.PolicyTagList(["projects/peace-demo/locations/us/taxonomies/1810677459816841425/policyTags/5146472154413249288"]))
create('peace-demo', "demo", "sample_table", [id_field, name_field])