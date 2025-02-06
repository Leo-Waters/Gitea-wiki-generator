from pathlib import Path
from pageGeneration import generate_pages
from DataModel import namespace_node
from ScriptParser import load_parsers
import glob
import os

def clear_output_folder(directory):

    print(f"clearing output folder: {directory}")

    files = glob.glob(os.path.join(directory, '*'))
    
    for file in files:
        try:
            if os.path.isfile(file):
                os.remove(file)
                print(f"Deleted file: {file}")
            else:
                print(f"Skipped non-file: {file}")
        except Exception as e:
            print(f"Error deleting file {file}: {e}")

parsers = load_parsers()

#using loaded parsers and associated extension, load and parse repo file contents 
for extention,parser in parsers.items():

    print(f"Testing {extention} parser")

    #initalize a root namespace
    root_namespace = namespace_node(name="root",desc="the root name space")

    file_path = Path(f"test/{extention}/test.{extention}")

    if file_path.exists():
        #parse test file
        parser.parse_file(file_path.as_posix(),root_namespace)
    else:
        print(f"File does not exist at: {file_path}")
        continue

    #generate and write pages to disk

    output_dir = Path(f"test/{extention}/output/")

    if output_dir.exists():
        clear_output_folder(output_dir)
        generate_pages(root_namespace,output_dir.as_posix()+"/")
        print(f"Generated {extention} test output at : {output_dir}")
    else:
        print(f"{extention} output directory does not exist at: {output_dir}")


