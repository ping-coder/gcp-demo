from google.cloud import datacatalog_v1

def create(
    taxonomy_name: str="projects/your-project-id/locations/us/taxonomies/[taxonomy-id]",
    parent_policy_tag: str=None, # resource name is similar as "projects/your-project-id/locations/us/taxonomies/[taxonomy-id]/policyTags/[policy-tag-id]"
    display_name: str="your-policy-tag-name"
):
    client = datacatalog_v1.PolicyTagManagerClient()
    request = datacatalog_v1.CreatePolicyTagRequest(
        parent = taxonomy_name,
        policy_tag = datacatalog_v1.PolicyTag(
            parent_policy_tag = parent_policy_tag,
            display_name=display_name,
        )
    )
    response = client.create_policy_tag(request=request)
    print(f"[policy_tag] Created policy tag, that display name is {response.display_name} and resouce name is {response.name}.")
    return response

def delete(
    name: str = "policy_tag_name"
):    
    client = datacatalog_v1.PolicyTagManagerClient()    
    # Initialize request argument(s)
    request = datacatalog_v1.DeletePolicyTagRequest(
        name=name,
    )
    taxonomy = client.delete_policy_tag(request=request)
    print(f"[policy_tag] Deleted policy tag's name is {name}.")
    return taxonomy

def find_one(
    taxonomy_name: str="projects/your-project-id/locations/us/taxonomies/[taxonomy-id]",
    display_name: str = "display-name"
):
    client = datacatalog_v1.PolicyTagManagerClient()
    # Initialize request argument(s)
    request = datacatalog_v1.ListPolicyTagsRequest(
        parent=taxonomy_name,
    )

    # Make the request
    page_result = client.list_policy_tags(request=request)

    # Handle the response
    for response in page_result:
        if(response.display_name==display_name):
            print(f"[policy_tag] Found a policy tag which display name is {display_name} and name is {response.name}.")
            return response
    print(f"[policy_tag] Not found any policy tag by display name '{display_name}'.")
    return None

def find_or_create(
    taxonomy_name: str="projects/your-project-id/locations/us/taxonomies/[taxonomy-id]",
    parent_policy_tag: str=None, # resource name is similar as "projects/your-project-id/locations/us/taxonomies/[taxonomy-id]/policyTags/[policy-tag-id]"
    display_name: str="your-policy-tag-name"
):
    tag = find_one(taxonomy_name=taxonomy_name, display_name=display_name)
    if(not tag):
        tag = create(taxonomy_name=taxonomy_name, parent_policy_tag=parent_policy_tag, display_name=display_name)
    return tag