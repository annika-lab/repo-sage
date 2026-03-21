import os
from git import Repo

def clone_repo(repo_url, clone_path="./repos"):
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_dir = os.path.join(clone_path, repo_name)

    if not os.path.exists(repo_dir):
        print(f"Cloning {repo_url}...")
        Repo.clone_from(repo_url, repo_dir)
    else:
        print("Repo already exists.")

    return repo_dir
