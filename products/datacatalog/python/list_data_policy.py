from google.cloud import bigquery_datapolicies_v1

def sample_list_data_policies():
    # Create a client
    client = bigquery_datapolicies_v1.DataPolicyServiceClient()

    # Initialize request argument(s)
    request = bigquery_datapolicies_v1.ListDataPoliciesRequest(
        parent=client.common_location_path(project='peace-demo', location='us'),
    )

    # Make the request
    page_result = client.list_data_policies(request=request)

    # Handle the response
    for response in page_result:
        print(response)

sample_list_data_policies()