import os
from dotenv import load_dotenv
import argparse
import csv
import requests
import base64

# Load environment variables from .env file
load_dotenv()

# Get the GitHub token from the environment
github_token = os.getenv("GITHUB_TOKEN")

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
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"Bearer {github_token}",
}

# Replace OWNER and REPO with appropriate values
owner = args.owner
repo = args.repo

# Getting the latest public key
response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/actions/secrets/public-key', headers=headers)

try:
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

            # Encode the secret value into base64
            secret_value_base64 = base64.b64encode(secret_value.encode()).decode()

            # Prepare data for the request
            data = {
                "encrypted_value": secret_value_base64,
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

except ValueError as e:
    print(f"Error while parsing JSON response: {e}")
except FileNotFoundError as e:
    print(f"File not found: {e}")
