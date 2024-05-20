from google.cloud import datacatalog_v1

def get_taxonomy_id(project_name):

    taxonomy_name = f"""{project_name}-auto-tagging-by-column-name-ui-created-tags"""

    client = datacatalog_v1.PolicyTagManagerClient()

    # Initialize request argument(s)
    request = datacatalog_v1.GetTaxonomyRequest(
        name=taxonomy_name,
    )
    response = client.get_taxonomy(request=request)

    taxonomy_id = response.name.split('/')[-1]

    print(f"Get taxonomy successfully, that taxonomy_id is {taxonomy_id}.")

    return taxonomy_id

get_taxonomy_id("peace-demo")