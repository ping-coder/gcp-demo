import taxonomy_client as t_client
import policy_tag_client as p_client
import constants as C

print(f"[GAMING DEMO] current project id is {C.DEFAULT_PROJECT_ID}.")
# create or find a taxonomy.
taxonomy = t_client.find_one(project_id=C.DEFAULT_PROJECT_ID, display_name=C.GAMING_TAXONOMY_DISPLAY_NAME)
if(not taxonomy):
    taxonomy = t_client.create(project_id=C.DEFAULT_PROJECT_ID, name=C.GAMING_TAXONOMY_DISPLAY_NAME)

# build a policy tags tree:
# -- PII
#    -- identification_number
#    -- passport_number
#    -- phone_number
#    -- full_name
#    -- email
#    -- address
# -- Financial
#    -- bank_account_number
#    -- credit_card_number
#    -- credit_card_expiration
#    -- credit_card_security_code
# -- Technical
#    -- ip_address
#    -- user_id
#    -- device_id
pii_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, display_name=C.GAMING_POLICY_TAG_PII)
identification_number_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, parent_policy_tag=pii_tag.name, display_name=C.GAMING_POLICY_TAG_IDENTIFICATION_NUMBER)
passport_number_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, parent_policy_tag=pii_tag.name, display_name=C.GAMING_POLICY_TAG_PASSPORT_NUMBER)
phone_number_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, parent_policy_tag=pii_tag.name, display_name=C.GAMING_POLICY_TAG_PHONE_NUMBER)
full_name_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, parent_policy_tag=pii_tag.name, display_name=C.GAMING_POLICY_TAG_FULL_NAME)
email_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, parent_policy_tag=pii_tag.name, display_name=C.GAMING_POLICY_TAG_EMAIL)
address_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, parent_policy_tag=pii_tag.name, display_name=C.GAMING_POLICY_TAG_ADDRESS)

financial_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, display_name=C.GAMING_POLICY_TAG_FINANCIAL)
bank_account_number_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, parent_policy_tag=financial_tag.name, display_name=C.GAMING_POLICY_TAG_BANK_ACCOUNT_NUMBER)
credit_card_number_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, parent_policy_tag=financial_tag.name, display_name=C.GAMING_POLICY_TAG_CREDIT_CARD_NUMBER)
credit_card_expiration_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, parent_policy_tag=financial_tag.name, display_name=C.GAMING_POLICY_TAG_CREDIT_CARD_EXPIRATION)
credit_card_security_code_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, parent_policy_tag=financial_tag.name, display_name=C.GAMING_POLICY_TAG_CREDIT_CARD_SECURITY_CODE)

technical_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, display_name=C.GAMING_POLICY_TAG_TECHNICAL)
ip_address_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, parent_policy_tag=technical_tag.name, display_name=C.GAMING_POLICY_TAG_IP_ADDRESS)
user_id_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, parent_policy_tag=technical_tag.name, display_name=C.GAMING_POLICY_TAG_USER_ID)
device_id_tag = p_client.find_or_create(taxonomy_name=taxonomy.name, parent_policy_tag=technical_tag.name, display_name=C.GAMING_POLICY_TAG_DEVICE_ID)