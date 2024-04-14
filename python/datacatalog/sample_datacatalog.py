import taxonomy_client as t_client
import policy_tag_client as p_client
import data_policy_client as d_client
from constants import *

import argparse
from google.cloud.bigquery_datapolicies_v1 import types

def run(
    project_id: str=DEFAULT_PROJECT_ID,
    is_delete: bool=True,
):
    # create a taxonomy named with 'test_taxonomy'
    taxonomy = t_client.find_or_create(project_id=project_id, name="sample_taxonomy")
    print(f"[sample] found or created a taxonomy: \r\n{taxonomy}")

    # get a taxonomy by taxonomy's resource name.
    get_taxonomy = t_client.get(taxonomy.name)
    print(f"[sample] got a taxonomy: \r\n{get_taxonomy}")

    # find a taxonomy by display name.
    find_taxonomy = t_client.find_one(project_id=project_id, display_name="test taxonomy")
    print(f"[sample] found a taxonomy: \r\n{find_taxonomy}")

    # create a policy tag.
    policy_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, display_name=GAMING_POLICY_TAG_PII, parent_policy_tag=None)
    print(f"[sample] found or created a policy tag: \r\n{policy_tag}")

    # find a policy tag by display name.
    find_policy_tag = p_client.find_one(taxonomy_name=taxonomy.name, display_name=policy_tag.display_name)
    print(f"[sample] found a policy tag: \r\n{find_policy_tag}")

    # create a data policy.
    data_policy = d_client.get_or_create(
        project_id=project_id,
        policy_tag=policy_tag.name,
        data_policy_id="sha256_policy",
    )
    print(f"[sample] Got or created a data policy: \r\n{data_policy}")

    # update the data policy to 
    new_data_policy = d_client.update(
        name=data_policy.name,
        policy_tag=data_policy.policy_tag,
        data_policy_type=data_policy.data_policy_type,
        predefined_expression=types.DataMaskingPolicy.PredefinedExpression.ALWAYS_NULL
    )
    print(f"[sample] Updateed the data policy: \r\n{new_data_policy}")

    # create or get the account table.
    

    if (is_delete):
        # delete the data policy
        d_client.delete(project_id=project_id,data_policy_id=data_policy.data_policy_id)
        # delete the policy tag.
        p_client.delete(policy_tag.name)
        # delete the taxonomy.
        t_client.delete(taxonomy.name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-p", "--project", help="Your Project ID.")
    parser.add_argument("-d", "--delete", action=argparse.BooleanOptionalAction, help="Ture|False, whether to delete resources.")
    parser.set_defaults(delete=True)
    
    args = parser.parse_args()
    
    if(not args.project):
        run(is_delete=args.delete)
    else:
        run(project_id=args.project, is_delete=args.delete)