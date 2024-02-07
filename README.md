# GitHub Secret Manager

This script is designed to add or update a secret in a GitHub repository using the GitHub API. It reads data from a CSV file and interacts with the GitHub API to manage repository secrets.

## Prerequisites

- Python 3.x
- Required Python packages can be installed using the following command:
  ```
  pip install -r requirements.txt
  ```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/arwahdevops/gh-secret-manager.git
   ```
2. Change the directory to the project folder:
   ```
   cd gh-secret-manager
   ```
3. Set up the environment by installing the required packages:
   ```
   pip install -r requirements.txt
   ```
## Setup GitHub Token

To use the script, you'll need to set up a `.env` file in the root directory of the project with the following content:
```
GITHUB_TOKEN=your_generated_token_here
```
Make sure to replace `your_generated_token_here` with the token you generated from GitHub.

## Example Usage

Organization :
```
python main.py -t org -o <organization> -f <file_name.csv>
```
Repository :
```
python main.py -t repo -o <owner> -r <repository> -f <file_name.csv>
```
- `-t` or `--type`: Specify the type of target (`org` for organization, `repo` for repository).
- `-o` or `--owner`: Specify the repository owner name.
- `-r` or `--repo`: Specify the repository name.
- `-f` or `--file`: Specify the CSV file name containing the secrets.

Make sure to replace `<organization>`, `<owner>`, `<repository>`, and `<file_name.csv>` with the appropriate values.

## License

This project is licensed under the [MIT License](LICENSE).
