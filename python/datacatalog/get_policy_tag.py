from google.cloud import datacatalog_v1

def get_policy_tag(
    project_id: str = "your-project-id",
    location_id: str = "us",
    taxonomy_id: str = "123456"
):
    client = datacatalog_v1.PolicyTagManagerClient()
     # Construct a full location path to be the parent of the taxonomy.
    parent = datacatalog_v1.PolicyTagManagerClient.common_location_path(
        project_id, location_id
    )
    # request = datacatalog_v1.CreatePolicyTagRequest(
    #     parent = "projects/peace-demo/locations/us/taxonomies/4992571310914755917",
    #     policy_tag = datacatalog_v1.PolicyTag(display_name="test policy tag")
    # )
    # response = client.create_policy_tag(request=request)

    # request = datacatalog_v1.GetTaxonomyRequest(
    #     name="8149809471608032745",
    # )
    
    # # TODO(developer): Construct a full Taxonomy object to send to the API.
    # taxonomy = datacatalog_v1.Taxonomy()
    # taxonomy.display_name = "test taxonomy"
    # taxonomy.description = "This Taxonomy represents ..."

    # # Send the taxonomy to the API for creation.
    # taxonomy = client.create_taxonomy(parent=parent, taxonomy=taxonomy)
    # print(f"Created taxonomy {taxonomy.name}")

    # request = datacatalog_v1.GetTaxonomyRequest(
    #     name="projects/peace-demo/locations/us/taxonomies/4992571310914755917",
    # )
    # response = client.get_taxonomy(request=request)

    # Initialize request argument(s)
    request = datacatalog_v1.GetPolicyTagRequest(
        name="projects/peace-demo/locations/us/taxonomies/4992571310914755917/policyTags/2253774803603369011",
    )

    # Make the request
    response = client.get_policy_tag(request=request)

    return response

print(get_policy_tag('peace-demo', 'us', '8149809471608032745'))