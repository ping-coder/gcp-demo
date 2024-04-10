from google.cloud import datacatalog_v1

def get_policy_tag(
    project_id: str = "your-project-id",
    location_id: str = "us",
    taxonomy_id: str = "123456"
):
    client = datacatalog_v1.PolicyTagManagerClient()

    request = datacatalog_v1.GetPolicyTagRequest(
        name="bigquery/policy-tags/locations/us/taxonomies/8149809471608032745",
    )

    response = client.get_policy_tag(request=request)

    return response

print(get_policy_tag('peace-demo', 'us', '8149809471608032745'))