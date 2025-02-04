import os
from pathlib import Path
from ScriptParser import *
from gitCommands import *
from fileLoading import *
from DataModel import namespace_node
from pageGeneration import generate_pages
if __name__ == "__main__":

    #ensure enviroment variables are set
    if "REPO_ADDRESS" in os.environ:
        raise Exception("enviroment variable not set: REPO_ADDRESS")
    
    if "WIKI_REPO_ADDRESS" in os.environ:
        raise Exception("enviroment variable not set: WIKI_REPO_ADDRESS")
    
    #load ignore list for file searching
    load_ignore_list()

    #get repo addresses from enviroment variables or .env file
    repo= os.getenv('REPO_ADDRESS')
    wikiRepo= os.getenv('WIKI_REPO_ADDRESS')

    print(f"Starting Auto Doc Generator\ntarget repo: {get_repo_name(repo)} for wiki at {wikiRepo} ")

    #get the latest repo files
    get_latest_repo(repo)
    
    #loading script paresers
    print("Loading Script Parser Modules")
    parsers = load_parsers()

    #create root namespace for all nodes
    root_node= namespace_node(name="root")

    #using loaded parsers and associated extension, load and parse repo file contents 
    for extention,parser in parsers.items():
        
        print(f"Loading {extention} files ")
        files = find_files_with_extension(Path("wkdir/"+get_repo_name(repo)),extention)

        for file in files:
            print(f"Parsing Script {file}")
            try:
                parser.parse_file(file,root_node)
            except:
                #need error colour
                print(f"Failed to parse {file}")
                pass
        
    root_node.debugChildren()

    #generate the wiki pages
    generate_pages(root_node,"wkdir/"+get_repo_name(wikiRepo))


    #push wiki update to git ##### TODO  ####