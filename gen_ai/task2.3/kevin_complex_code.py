import os
import certifi
import plaid
import logging
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.exceptions import ApiException

# Ensure SSL certificates are correctly configured
os.environ["SSL_CERT_FILE"] = certifi.where()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Retrieve API keys from environment variables
CLIENT_ID = os.getenv("PLAID_CLIENT_ID", "")
SECRET = os.getenv("PLAID_SECRET", "")

if not CLIENT_ID or not SECRET:
    logging.error("Missing Plaid API credentials. Set PLAID_CLIENT_ID and PLAID_SECRET in environment variables.")
    exit(1)

def get_plaid_client():
    """Set up and return a Plaid API client."""
    configuration = plaid.Configuration(
        host=plaid.Environment.Sandbox,  # Change this for production use
        api_key={"clientId": CLIENT_ID, "secret": SECRET},
    )
    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)

def create_link_token():
    """Creates and returns a Plaid Link token."""
    client = get_plaid_client()
    request = LinkTokenCreateRequest(
        user=LinkTokenCreateRequestUser(client_user_id="user-12345"),
        client_name="My Expense Tracker",
        products=[Products("transactions")],
        country_codes=[CountryCode("US")],
        language="en"
    )

    try:
        response = client.link_token_create(request)
        logging.info("Link token successfully created.")
        return response.to_dict()
    except ApiException as e:
        logging.error(f"Plaid API error: {e}")
        return None

if __name__ == "__main__":
    link_token = create_link_token()
    if link_token:
        logging.info(f"Generated Link Token: {link_token['link_token']}")