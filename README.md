# Bitbucket to GitHub Migration Script

This Python script helps migrate repositories from Bitbucket to GitHub.

## Requirements

- Python 3.6+
- Git command-line tool installed
- [GitHub CLI tool (gh)](https://github.com/cli/cli#installation) installed and authenticated
- Access to the Bitbucket and GitHub repositories that you want to clone and push
- SSH keys configured for both Bitbucket and GitHub

## Usage

1. Update the `config.py` file with your Bitbucket organization (`bitbucket_org`), GitHub organization (`github_org`), and the list of repositories (`bitbucket_repos`) you want to migrate.

    Example:

    ```python
    bitbucket_org = 'bitbucket_org_name'
    github_org = 'github_org_name'
    bitbucket_repos = ['repo1', 'repo2', 'repo3']
    ```

2. Run the script using Python 3:

    ```bash
    python bb2gh.py
    ```

The script will clone each repository from Bitbucket, create a new repository under the given GitHub organization, and push the repository to GitHub. This is done using the `--mirror` option in Git, which ensures that all branches and commits are transferred as-is.

If an error occurs during the process (for example, due to a failed command), the script will print an error message and prompt the user to either continue with the next repository ('c') or stop the execution ('s').

## Notes

- The script assumes that you have the necessary permissions to clone the repositories from Bitbucket and create repositories in the specified GitHub organization.
- The script uses `os.chdir()` to change the working directory. Please run the script from a directory where you have permissions to create and delete files.
- The script will delete the local cloned Bitbucket repository directory after pushing to GitHub, regardless of success.
- This script uses the `gh` command-line tool to create a new private repository on GitHub. You will need to authenticate `gh` before running the script.

## License

This script is licensed under the MIT License. You are free to use, modify, and distribute the script in accordance with the terms of this license.