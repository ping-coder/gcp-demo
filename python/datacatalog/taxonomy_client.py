from google.cloud import datacatalog_v1

def create(
    project_id: str = "your-project-id",
    location_id: str = "us",
    name: str = "display-name",
    description: str = ""
):
    client = datacatalog_v1.PolicyTagManagerClient()
    parent = client.common_location_path(
        project_id, location_id
    )
    taxonomy = datacatalog_v1.Taxonomy()
    taxonomy.display_name = name
    taxonomy.description = description

    # # Send the taxonomy to the API for creation.
    taxonomy = client.create_taxonomy(parent=parent, taxonomy=taxonomy)
    print(f"[taxonomy] Created taxonomy name is {taxonomy.name}.")
    return taxonomy

def get(
    name: str = "taxonomy_name"
):    
    client = datacatalog_v1.PolicyTagManagerClient()    
    # Initialize request argument(s)
    request = datacatalog_v1.GetTaxonomyRequest(
        name=name,
    )
    taxonomy = client.get_taxonomy(request=request)
    print(f"[taxonomy] Get taxonomy name is {taxonomy.name}.")
    return taxonomy

def delete(
    name: str = "taxonomy_name"
):    
    client = datacatalog_v1.PolicyTagManagerClient()    
    # Initialize request argument(s)
    request = datacatalog_v1.DeleteTaxonomyRequest(
        name=name,
    )
    taxonomy = client.delete_taxonomy(request=request)
    print(f"[taxonomy] Deleted taxonomy name is {name}.")
    return taxonomy

def find_one(
    project_id: str = "your-project-id",
    location_id: str = "us",
    display_name: str = "display-name"
):
    client = datacatalog_v1.PolicyTagManagerClient()
    parent = client.common_location_path(
        project_id, location_id
    )
    # Initialize request argument(s)
    request = datacatalog_v1.ListTaxonomiesRequest(
        parent=parent,
    )

    # Make the request
    page_result = client.list_taxonomies(request=request)

    # Handle the response
    for response in page_result:
        if(response.display_name==display_name):
            print(f"[taxonomy] Found a taxonomy which display name is {display_name} and name is {response.name}.")
            return response
    print(f"[taxonomy] Not found any taxonomy by display name '{display_name}'.")
    return None

def find_or_create(
    project_id: str = "your-project-id",
    location_id: str = "us",
    name: str = "display-name",
    description: str = ""
):
    taxonomy = find_one(project_id=project_id,location_id=location_id,display_name=name)
    if(not taxonomy):
        taxonomy = create(project_id=project_id,location_id=location_id,name=name,description=description)
    return taxonomy