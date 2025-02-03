import os
from pathlib import Path
import subprocess

#Get the latest repo from the address
def get_latest_repo(address):
    if(clone_exists(address)):
        print(f"{get_repo_name(address)} already exists, pulling repo updates from {address}")
        #pull latests branch updates
        pulledRepo=False
        attemptsLeft=5
        while(pulledRepo==False and attemptsLeft>0):
            print(f"pulling repo {attemptsLeft} attempts left")
            pulledRepo=pull_repo(address,"wkdir/"+get_repo_name(address))
            attemptsLeft=attemptsLeft-1

        if(pulledRepo==False):
            raise Exception("Could not Pull Repo")
        
    else:
        print(f"{get_repo_name(address)} doesnt exist, cloneing repo from {address}")
        #clone the latest branch

        clonedRepo=False
        attemptsLeft=5
        while(clonedRepo==False and attemptsLeft>0):
            print(f"cloning repo {attemptsLeft} attempts left")
            clonedRepo=clone_repo(address,"wkdir/"+get_repo_name(address))
            attemptsLeft=attemptsLeft-1

        if(clonedRepo==False):
            raise Exception("Could not Clone Repo")

#clone the repo from the url to the local clone directory
def clone_repo(repo_url, clone_dir):
    try:
        result = subprocess.run(['git', 'clone', repo_url, clone_dir], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            print("Repository cloned successfully!")
            return True
        else:
            print("Failed to clone the repository.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr.decode('utf-8')}")
        return False

#pull the repo from the url to the local repo
def pull_repo(repo_url, clone_dir):
    try:
        result = subprocess.run(['git', 'pull',repo_url,'-origin'], cwd=clone_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            print("Repository updated successfully!")
            return True
        else:
            print("Failed to update the repository.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr.decode('utf-8')}")
        return False

#does a clone of the repo adress already exist
def clone_exists(address):
    return Path("wkdir/"+get_repo_name(address)).exists()

#gets the name of the repo from the address
def get_repo_name(address):
    file_path = Path(address)
    return file_path.stem