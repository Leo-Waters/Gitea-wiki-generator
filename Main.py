import os
from pathlib import Path
import subprocess

import importlib
import inspect
import pkgutil
from pathlib import Path
from modules import __name__ as modules_package_name
from ScriptParser import ScriptParser
from DataModel import namespace_node


def load_parsers(modules_path, base_class):
    parsers = {}
    for _, module_name, _ in pkgutil.iter_modules([modules_path]):
        module = importlib.import_module(f"{modules_package_name}.{module_name}")
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Check if it is a subclass of the base class and not the base class itself
            if issubclass(obj, base_class) and obj is not base_class:
                instance = obj()  # Instantiate the parser
                parsers[instance.language] = instance  # Store the instance in the dictionary
                print(f"Loaded parser for language: {instance.language}")
    return parsers



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


def clone_exists():
    return Path("wkdir/"+get_repo_name()).exists()

#gets the name of the repo from the address
def get_repo_name():
    file_path = Path(os.getenv('REPO_ADDRESS'))
    return file_path.stem

def find_files_with_extension(directory, extension):
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                matching_files.append(os.path.join(root, file))
    return matching_files


def GetLatestRepo(repo):
    if(clone_exists()):
        print(f"{get_repo_name()} already exists, pulling repo updates from {repo}")
        #pull latests branch updates
        pulledRepo=False
        attemptsLeft=5
        while(pulledRepo==False and attemptsLeft>0):
            print(f"pulling repo {attemptsLeft} attempts left")
            pulledRepo=pull_repo(repo,"wkdir/"+get_repo_name())
            attemptsLeft=attemptsLeft-1

        if(pulledRepo==False):
            raise Exception("Could not Pull Repo")
        
    else:
        print(f"{get_repo_name()} doesnt exist, cloneing repo from {repo}")
        #clone the latest branch

        clonedRepo=False
        attemptsLeft=5
        while(clonedRepo==False and attemptsLeft>0):
            print(f"cloning repo {attemptsLeft} attempts left")
            clonedRepo=clone_repo(repo,"wkdir/"+get_repo_name())
            attemptsLeft=attemptsLeft-1

        if(clonedRepo==False):
            raise Exception("Could not Clone Repo")

if __name__ == "__main__":
    print("Starting Auto Doc Generator")
    repo= os.getenv('REPO_ADDRESS')
    wikiRepo= os.getenv('WIKI_REPO_ADDRESS')
    print(f"target repo: {get_repo_name()} for wiki at {wikiRepo}")

    GetLatestRepo(repo)
        
    #now that we have all the project files we can parse the code base for code descriptors

    print("Loading Script Parser Modules")
    modules_path = Path(__file__).parent / "modules"
    parsers = load_parsers(str(modules_path), ScriptParser)



    root_node= namespace_node()

    for extention,parser in parsers.items():
        
        print(f"Loading {extention} files ")
        files = find_files_with_extension(Path("wkdir/"+get_repo_name()),extention)

        for file in files:
            print(f"Parsing Script {file}")
            try:
                parser.parse_file(file,namespaces)
            except:
                #need error colour
                print(f"Failed to parse {file}")
                pass