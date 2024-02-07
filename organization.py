import os
import csv
import requests
from base64 import b64encode, b64decode
from nacl import public
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def encrypt(public_key: str, secret_value: str) -> str:
    public_key_bytes = b64decode(public_key.encode("utf-8"))
    if len(public_key_bytes) != 32:
        raise ValueError("Invalid public key length")

    public_key_obj = public.PublicKey(public_key_bytes)
    sealed_box = public.SealedBox(public_key_obj)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")

def get_public_key(organization: str, headers: dict) -> dict:
    try:
        # Get the latest public key for the organization
        response = requests.get(f'https://api.github.com/orgs/{organization}/actions/secrets/public-key', headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Convert response to JSON format
        public_key_response = response.json()

        return public_key_response

    except requests.exceptions.RequestException as e:
        print(f"Error in getting the public key: {e}")
        raise

def add_or_update_org_secret(organization: str, file: str):
    # Set up GitHub token
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
    }

    try:
        public_key_response = get_public_key(organization, headers)

        # Extracting the key from the response
        public_key = public_key_response['key']

        # Read data from the CSV file
        with open(file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                secret_name = row['secret_name']
                secret_value = row['secret_value']

                # Encrypt the secret value using the GitHub public key
                encrypted_secret = encrypt(public_key, secret_value)

                # Prepare data for the request
                data = {
                    "encrypted_value": encrypted_secret,
                    "key_id": public_key_response['key_id'],
                    "visibility": "private"  # Add the visibility parameter
                }

                # Send a PUT request to the GitHub API to update the secret for the organization
                response = requests.put(f'https://api.github.com/orgs/{organization}/actions/secrets/{secret_name}', headers=headers, json=data)

                # Check the status code
                if response.status_code == 201:
                    print(f"Secret {secret_name} for organization {organization} successfully added.")
                elif response.status_code == 204:
                    print(f"Secret {secret_name} for organization {organization} successfully updated.")
                else:
                    print(f"Error message: {response.text}")

    except Exception as e:
        print(f"Unexpected error occurred: {e}")