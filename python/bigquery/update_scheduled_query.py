from google.cloud import bigquery_datatransfer
from google.protobuf import field_mask_pb2

transfer_client = bigquery_datatransfer.DataTransferServiceClient()

# The project where the query job runs is the same as the project
# containing the destination dataset.
project_id = "peace-demo"
dataset_id = "demo"

# Use standard SQL syntax for the query.
# query_string = """
# SELECT
#   CURRENT_TIMESTAMP() as current_time,
#   @run_time as intended_run_time,
#   @run_date as intended_run_date,
#   17 as some_integer
# """
query_string ="""
CREATE OR REPLACE FUNCTION `peace-demo.demo.SSN_Mask`(ssn STRING) RETURNS STRING
OPTIONS (data_governance_type="DATA_MASKING") AS (
CAST(SHA256(CONCAT(ssn, '12345678-a997-438b-a863-15263d319353')) AS STRING format 'HEX')
);
"""

parent = transfer_client.common_location_path(project_id, "us")
# parent = transfer_client.common_project_path(project_id)

transfer_config = bigquery_datatransfer.TransferConfig(
    name = "projects/642598805451/locations/us/transferConfigs/663bd0e9-0000-2d85-b211-582429afd714",
    # destination_dataset_id=dataset_id,
    display_name="Test Scheduled Query Name",
    data_source_id="scheduled_query",
    params={
        "query": query_string,
        # "destination_table_name_template": "test_table_{run_date}",
        # "write_disposition": "WRITE_TRUNCATE",
        # "partitioning_field": "",
    },
    schedule="every 24 hours",
)

transfer_config = transfer_client.update_transfer_config(
    bigquery_datatransfer.UpdateTransferConfigRequest(
        transfer_config=transfer_config,
        update_mask=field_mask_pb2.FieldMask(paths=["params"])
    )
)

print("Created scheduled query '{}'".format(transfer_config.name))