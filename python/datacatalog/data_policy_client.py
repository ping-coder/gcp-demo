from google.cloud import bigquery_datapolicies_v1
from google.cloud.bigquery_datapolicies_v1 import types
from google.api_core import exceptions

def create(
    project_id: str = "your-project-id",
    location_id: str = "us",
    policy_tag: str = None, # Policy tag resource name, in the format of projects/{project_number}/locations/{location_id}/taxonomies/{taxonomy_id}/policyTags/{policyTag_id}.
    data_policy_id: str = "your-policy-id", # Used as {data_policy_id} in part of the resource name.
    data_policy_type: bigquery_datapolicies_v1.DataPolicy.DataPolicyType = bigquery_datapolicies_v1.DataPolicy.DataPolicyType.DATA_MASKING_POLICY, # Type of data policy.
    predefined_expression: types.DataMaskingPolicy.PredefinedExpression = types.DataMaskingPolicy.PredefinedExpression.SHA256, # A predefined masking expression.
    routine: str = None, # The name of the BigQuery routine that contains the custom masking routine, in the format of projects/{project_number}/datasets/{dataset_id}/routines/{routine_id}.
):
    # Create a client
    client = bigquery_datapolicies_v1.DataPolicyServiceClient()

    # Initialize data policy object
    data_policy = bigquery_datapolicies_v1.DataPolicy()
    data_policy.data_policy_type = data_policy_type
    data_policy.data_policy_id = data_policy_id
    data_policy.policy_tag = policy_tag
    if(not routine and routine is not None):
        data_policy.data_masking_policy.routine = routine
    else:
        data_policy.data_masking_policy.predefined_expression = predefined_expression

    # Initialize request argument(s)
    request = bigquery_datapolicies_v1.CreateDataPolicyRequest(
        parent=client.common_location_path(project=project_id, location=location_id),
        data_policy=data_policy,
    )

    response = client.create_data_policy(request=request)
    print(f"[data_policy] Created data policy, that data policy tag is {data_policy} and name is {response.name}.")
    return response

def delete(
    project_id: str = "your-project-id",
    location_id: str = "us",
    data_policy_id: str = "your-policy-id", # Used as {data_policy_id} in part of the resource name.
):
    # Create a client
    client = bigquery_datapolicies_v1.DataPolicyServiceClient()

     # Initialize request argument(s)
    request = bigquery_datapolicies_v1.DeleteDataPolicyRequest(
        name=client.data_policy_path(project=project_id, location=location_id, data_policy=data_policy_id)
    )
    client.delete_data_policy(request=request)
    print(f"[data_policy] Deleted data policy, data policy id is {data_policy_id}.")

def get(
    project_id: str = "your-project-id",
    location_id: str = "us",
    data_policy_id: str = "your-data-policy-id", # Used as {data_policy_id} in part of the resource name.
):
    # Create a client
    client = bigquery_datapolicies_v1.DataPolicyServiceClient()

     # Initialize request argument(s)
    request = bigquery_datapolicies_v1.GetDataPolicyRequest(
        name=client.data_policy_path(project=project_id, location=location_id, data_policy=data_policy_id)
    )
    try:
        data_policy = client.get_data_policy(request=request)
        print(f"[data_policy] Get data policy name is {data_policy.name}.")
        return data_policy
    except (exceptions.NotFound):
        print(f"[data_policy] Not found any data policy by id '{data_policy_id}'.")
        return None

def get_or_create(
    project_id: str = "your-project-id",
    location_id: str = "us",
    data_policy_id: str = "your-policy-id", # Used as {data_policy_id} in part of the resource name.
    policy_tag: str = None, # Policy tag resource name, in the format of projects/{project_number}/locations/{location_id}/taxonomies/{taxonomy_id}/policyTags/{policyTag_id}.
    data_policy_type: bigquery_datapolicies_v1.DataPolicy.DataPolicyType = bigquery_datapolicies_v1.DataPolicy.DataPolicyType.DATA_MASKING_POLICY, # Type of data policy.
    predefined_expression: types.DataMaskingPolicy.PredefinedExpression = types.DataMaskingPolicy.PredefinedExpression.SHA256, # A predefined masking expression.
    routine: str = None, # The name of the BigQuery routine that contains the custom masking routine, in the format of projects/{project_number}/datasets/{dataset_id}/routines/{routine_id}.
):
    data_policy = get(project_id=project_id,location_id=location_id,data_policy_id=data_policy_id)
    if(not data_policy):
        data_policy = create(
            project_id=project_id,location_id=location_id,data_policy_id=data_policy_id,
            policy_tag=policy_tag, data_policy_type=data_policy_type, predefined_expression=predefined_expression, routine=routine,
        )
    return data_policy

def update(
    name: str= None, # Resource name of this data policy, in the format of projects/{project_number}/locations/{location_id}/dataPolicies/{data_policy_id}.
    policy_tag: str = None, # Policy tag resource name, in the format of projects/{project_number}/locations/{location_id}/taxonomies/{taxonomy_id}/policyTags/{policyTag_id}.
    data_policy_type: bigquery_datapolicies_v1.DataPolicy.DataPolicyType = bigquery_datapolicies_v1.DataPolicy.DataPolicyType.DATA_MASKING_POLICY, # Type of data policy.
    predefined_expression: types.DataMaskingPolicy.PredefinedExpression = types.DataMaskingPolicy.PredefinedExpression.SHA256, # A predefined masking expression.
    routine: str = None, # The name of the BigQuery routine that contains the custom masking routine, in the format of projects/{project_number}/datasets/{dataset_id}/routines/{routine_id}.
):
    # Create a client
    client = bigquery_datapolicies_v1.DataPolicyServiceClient()

    # Initialize request argument(s)
    data_policy = bigquery_datapolicies_v1.DataPolicy()    
    data_policy.data_policy_type = data_policy_type
    data_policy.name = name
    data_policy.policy_tag = policy_tag
    if(not routine and routine is not None):
        data_policy.data_masking_policy.routine = routine
    else:
        data_policy.data_masking_policy.predefined_expression = predefined_expression

    request = bigquery_datapolicies_v1.UpdateDataPolicyRequest(
        data_policy=data_policy,
    )

    # Make the request
    response = client.update_data_policy(request=request)
    print(f"[data_policy] Updated data policy name is {data_policy.name}.")
    return response
