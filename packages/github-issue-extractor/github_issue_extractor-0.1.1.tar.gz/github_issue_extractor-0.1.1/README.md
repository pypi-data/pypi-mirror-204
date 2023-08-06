# GitHub Issue Extractor

This script extracts all issues from a specified milestone in a GitHub repository and saves them to an Excel file. The script can be run from the command line and accepts the milestone number and access token as arguments.

## Requirements

- Python 3.6 or higher
- requests module
- openpyxl module

## Installation

1. Clone the GitHub repository to your local machine.
2. Install the required modules using pip: `pip install -r requirements.txt`

## Usage

To run the script, use the following command:

`python main.py <milestone_number> <access_token> <repo-name> <name_of_owner_of_the_repo>`


Replace `<milestone_number>` with the number of the milestone you want to extract issues from, `<access_token>` with your GitHub access token, `<repo-name>` with the repo name, and `<name_of_owner_of_the_repo>` with the name of the owner of the repository.

Example:

`python main.py 1 abc123def456 issues-repo-name owner_of_the_repo`



This will extract all issues from milestone 1 in the specified repository and save them to an Excel file.

The Excel file will be saved as `<reponame>-<milestone_number>.xlsx` in the Downloads folder.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
