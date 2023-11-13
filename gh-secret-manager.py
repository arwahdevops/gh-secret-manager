import os
from dotenv import load_dotenv
import argparse
import csv
import requests
from base64 import b64encode, b64decode
from nacl import public

# Load environment variables from .env file
load_dotenv()

# Function to encrypt a secret value using the GitHub public key
def encrypt(public_key: str, secret_value: str) -> str:
    public_key_bytes = b64decode(public_key.encode("utf-8"))
    if len(public_key_bytes) != 32:
        raise ValueError("Invalid public key length")
    
    public_key_obj = public.PublicKey(public_key_bytes)
    sealed_box = public.SealedBox(public_key_obj)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")

# Parsing command-line arguments
parser = argparse.ArgumentParser(description='Script to add or update a secret in a GitHub repository.')
parser.add_argument('-o', '--owner', type=str, help='Repository owner name')
parser.add_argument('-r', '--repo', type=str, help='Repository name')
parser.add_argument('-f', '--file', type=str, help='CSV file name')
args = parser.parse_args()

# Additional validation for required arguments
if not (args.owner and args.repo and args.file):
    parser.print_help()
    exit(1)

# Set up GitHub token
github_token = os.getenv("GITHUB_TOKEN")
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {github_token}",
}

# Replace OWNER and REPO with appropriate values
owner = args.owner
repo = args.repo

# Getting the latest public key
try:
    response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/actions/secrets/public-key', headers=headers)
    response.raise_for_status()  # Raise an HTTPError for bad responses

    # Convert response to JSON format
    public_key_response = response.json()

    # Extracting the key from the response
    public_key = public_key_response['key']

    # Read data from the CSV file
    with open(args.file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            secret_name = row['secret_name']
            secret_value = row['secret_value']

            # Enkripsi nilai secret menggunakan kunci publik GitHub
            encrypted_secret = encrypt(public_key, secret_value)

            # Prepare data for the request
            data = {
                "encrypted_value": encrypted_secret,
                "key_id": public_key_response['key_id']
            }

            # Send a PUT request to the GitHub API to update the secret
            response = requests.put(f'https://api.github.com/repos/{owner}/{repo}/actions/secrets/{secret_name}', headers=headers, json=data)

            # Check the status code
            if response.status_code == 201:
                print(f"Secret {secret_name} successfully added.")
            elif response.status_code == 204:
                print(f"Secret {secret_name} successfully updated.")
            else:
                print(f"Error message: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Error in making the request: {e}")
except ValueError as e:
    print(f"Error: {e}")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except Exception as e:
    print(f"Unexpected error occurred: {e}")
