from github import Github
from github import Auth
from git import Repo
import os
from pathlib import Path
from enum import Enum

# Configuration file (config.py)
GITHUB_API_KEY = "your access token "
GITHUB_TEMPLATES_DIR = "your temp directory"
TEMP_PROJECT_DIR = "your project temp directory"


# Authenticate with GitHub using your API key
smth_auth = Auth.Token(GITHUB_API_KEY)
smth_github = Github(auth=smth_auth)


class Language(str, Enum):
    python = "python"
    astro_js = "astro"

    def __str__(self):
        return self.value


def add_gitignore(dir_filepath: str | Path, language: str):
    """
    Add a .gitignore file to the specified directory.

    :param dir_filepath: The directory to add the .gitignore file to.
    :param language: The language to use for the .gitignore file.
    """
    # Ensure the filepath is a Path object
    if not isinstance(dir_filepath, Path):
        dir_filepath = Path(dir_filepath)

    # Create the .gitignore file
    gitignore_filepath = dir_filepath / ".gitignore"

    # Open gitignore template from app.services.github.templates folder
    try:
        gitignore_template = open(Path(GITHUB_TEMPLATES_DIR) / f"{language}_gitignore").read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find gitignore template for {language}")

    with open(gitignore_filepath, "w") as f:
        f.write(gitignore_template)

def create_repo(repo_name: str, temp_dir_name: str, language: Language, github_user: Github = smth_github):
    new_repo = github_user.get_user().create_repo(repo_name)

    temp_filepath = os.path.join(TEMP_PROJECT_DIR, temp_dir_name)
    os.chdir(temp_filepath)

    # Create the ./src directory if it doesn't exist
    src_directory = os.path.join(temp_filepath, "src")
    if not os.path.isdir(src_directory):
        os.mkdir(src_directory)

    assert os.path.isdir("./src")

    if not os.path.isfile(".gitignore"):
        add_gitignore(temp_filepath, language)

    # Initialize the repo
    repo = Repo.init(temp_filepath)
    open(os.path.join(temp_filepath, "README.md"), "w").close()
       # Perform an initial commit
    repo.index.add(["README.md"])
    repo.index.commit("Initial commit 🌱")
    # Add all the files in the current directory
    repo.git.add(all=True)

    # Check if there are changes staged for commit
    if repo.git.status('--porcelain'):
        # Commit the changes
        repo.git.commit('-m', 'Initial commit 🌱')
        # Set the remote origin and push
        origin = repo.create_remote('origin', new_repo.clone_url)
        origin.push(refspec='{}:{}'.format(repo.active_branch, repo.active_branch))
    else:
        print("No changes to commit")

    # Clone the repository locally
    local_clone_path = os.path.join("C:\\Users\\jdarj\\Downloads\\Upwork-client\\python-upload-deploy-script\\tmp_dir\\", temp_dir_name)
    local_repo = Repo.clone_from(new_repo.clone_url, local_clone_path)

    # Copy the files you want to add or modify into the local clone (e.g., copy your files into /path/to/your/local/clone/my-temp-directory/src/)
    # For example, to add a new file called "new_file.py":
    new_file_content = "print('Hello, World!')"
    with open(os.path.join(local_clone_path, "src", "new_file.py"), "w") as new_file:
        new_file.write(new_file_content)

    # Modify an existing file (e.g., main.py)
    modified_file_path = os.path.join(local_clone_path, "src", "main.py")
    with open(modified_file_path, "a") as modified_file:
        modified_file.write("\n# This is a modification!")

    # Stage the changes
    local_repo.git.add(all=True)

    # Commit the changes
    local_repo.git.commit('-m', 'Adding and modifying files')

    # Push the changes back to the remote repository
    local_repo.git.push()

    return new_repo.clone_url


if __name__ == "__main__":
    # Sample values
    repo_name = "my_new_repo"
    temp_dir_name = "my_temp_directory"
    chosen_language = Language.python
  

    # Create the repository, commit initial changes, and add additional files
    created_repo_url = create_repo(repo_name, temp_dir_name, chosen_language)
    print(f"Repository created: {created_repo_url}")
