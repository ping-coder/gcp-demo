from google.cloud import bigquery_datatransfer

transfer_client = bigquery_datatransfer.DataTransferServiceClient()

project_id = "peace-demo"
parent = transfer_client.common_project_path(project_id)

configs = transfer_client.list_transfer_configs(parent=parent)
print("Got the following configs:")
for config in configs:
    print(f"\tID: {config.name}, Schedule: {config.schedule}, Sql: {config.params.__dict__}")