import os
import json

from google.cloud import bigquery

def get_project_id():
    # In python 3.7, this works
    project_id = os.getenv("GCP_PROJECT")
    
    if not project_id:  # get env project id
        project_id = os.getenv("DEFAULT_PROJECT_ID")
        print(f"[constants] Get project id from env: {project_id}.")

    if not project_id:  # Running locally
        with open(os.environ["GOOGLE_APPLICATION_CREDENTIALS"], "r") as fp:
            credentials = json.load(fp)
        project_id = credentials["project_id"]
        print("[constants] Get project id from credentials file.")

    if not project_id:  # > python37
        # Only works on runtime.
        import urllib.request

        url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
        req = urllib.request.Request(url)
        req.add_header("Metadata-Flavor", "Google")
        project_id = urllib.request.urlopen(req).read().decode()
        print("[constants] Get project id from http://metadata.google.internal.")

    if not project_id:
        raise ValueError("[constants] Could not get a value for PROJECT_ID")

    return project_id

# default project and location
DEFAULT_PROJECT_ID = get_project_id()
DEFAULT_LOCATION = "us"

# gaming demo - taxonomy
GAMING_TAXONOMY_DISPLAY_NAME = "Gaming Demo"

# gaming demo - policy tag
GAMING_POLICY_TAG_PII = "PII"
GAMING_POLICY_TAG_IDENTIFICATION_NUMBER = "identification_number"
GAMING_POLICY_TAG_PASSPORT_NUMBER = "passport_number"
GAMING_POLICY_TAG_PHONE_NUMBER = "phone_number"
GAMING_POLICY_TAG_FULL_NAME = "full_name"
GAMING_POLICY_TAG_EMAIL = "email"
GAMING_POLICY_TAG_ADDRESS = "address"

GAMING_POLICY_TAG_FINANCIAL = "Financial"
GAMING_POLICY_TAG_BANK_ACCOUNT_NUMBER = "bank_account_number"
GAMING_POLICY_TAG_CREDIT_CARD_NUMBER = "credit_card_number"
GAMING_POLICY_TAG_CREDIT_CARD_EXPIRATION = "credit_card_expiration"
GAMING_POLICY_TAG_CREDIT_CARD_SECURITY_CODE = "credit_card_security_code"

GAMING_POLICY_TAG_TECHNICAL = "Technical"
GAMING_POLICY_TAG_IP_ADDRESS = "ip_address"
GAMING_POLICY_TAG_USER_ID = "user_id"
GAMING_POLICY_TAG_DEVICE_ID = "device_id"

# gaming demo - table
GAMING_TABLE_FIELD_CREATION_TIME = bigquery.SchemaField(name="creation_time", field_type="DATE_TIME", mode="REQUIRED")

id_field = bigquery.SchemaField(name="id", field_type="STRING", mode="REQUIRED")
name_field = bigquery.SchemaField(name="email", field_type="STRING", mode="REQUIRED", policy_tags=bigquery.PolicyTagList(["projects/peace-demo/locations/us/taxonomies/1810677459816841425/policyTags/5146472154413249288"]))

GAMING_TABLE_ACCOUNT = bigquery.SchemaField(name="t_account", field_type="STRING", mode="REQUIRED")
GAMING_TABLE_ACCOUNT_UID = "uid"
GAMING_TABLE_ACCOUNT_EMAIL = "email"
GAMING_TABLE_ACCOUNT_PHONE_NUMBER = "phone_number"