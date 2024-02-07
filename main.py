import argparse
from repositories import add_or_update_repo_secret
from organization import add_or_update_org_secret

def main():
    # Parsing command-line arguments
    parser = argparse.ArgumentParser(description='Script to add or update a secret in a GitHub repository or organization.')
    parser.add_argument('-t', '--type', choices=['repo', 'org'], help='Specify whether to work with a repository or organization')
    parser.add_argument('-o', '--owner', type=str, help='Owner name')
    parser.add_argument('-r', '--repo', type=str, help='Repository name')
    parser.add_argument('-f', '--file', type=str, help='CSV file name')
    args = parser.parse_args()

    # Additional validation for required arguments
    if not (args.type and args.owner and args.file):
        parser.print_help()
        exit(1)

    if args.type == 'repo':
        add_or_update_repo_secret(args.owner, args.repo, args.file)
    elif args.type == 'org':
        add_or_update_org_secret(args.owner, args.file)

if __name__ == "__main__":
    main()
