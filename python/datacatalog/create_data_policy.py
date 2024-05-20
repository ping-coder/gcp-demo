from google.cloud import bigquery_datapolicies_v1

def sample_create_data_policy():
    # Create a client
    client = bigquery_datapolicies_v1.DataPolicyServiceClient()

    # Initialize request argument(s)
    data_policy = bigquery_datapolicies_v1.DataPolicy()
    data_policy.data_policy_type = bigquery_datapolicies_v1.DataPolicy.DataPolicyType.DATA_MASKING_POLICY
    data_policy.name = "projects/peace-demo/locations/us/dataPolicies/test12"
    data_policy.data_policy_id = "test12"
    data_policy.policy_tag = "projects/peace-demo/locations/us/taxonomies/4992571310914755917/policyTags/2253774803603369011"
    data_policy.data_masking_policy.predefined_expression = "DATE_YEAR_MASK"
    # data_policy.data_masking_policy.routine = "projects/642598805451/datasets/demo/routines/SSN_Mask"

    request = bigquery_datapolicies_v1.CreateDataPolicyRequest(
        parent = client.common_location_path(project='peace-demo', location='us'),
        data_policy=data_policy,
    )

    # Make the request
    response = client.create_data_policy(request=request)

    # Handle the response
    print(response)

sample_create_data_policy()