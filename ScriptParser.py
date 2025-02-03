from pathlib import Path
import importlib
import inspect
import pkgutil
from modules import __name__ as modules_package_name

#retuns an array of lanuguage parsers, loaded from the /modules folder
def load_parsers():
    modules_path=Path(__file__).parent / "modules"
    parsers = {}
    for _, module_name, _ in pkgutil.iter_modules([modules_path]):
        module = importlib.import_module(f"{modules_package_name}.{module_name}")
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Check if it is a subclass of the base class and not the base class itself
            if issubclass(obj, ScriptParser) and obj is not ScriptParser:
                instance = obj()  # Instantiate the parser
                parsers[instance.language] = instance  # Store the instance in the dictionary
                print(f"Loaded parser for language: {instance.language}")
    return parsers

#base class for script parsers
class ScriptParser:
    def __init__(self,language):
        self.language=language
    
    #loads the contents of a file as a string
    @staticmethod
    def _load_from_file(filePath):
        return Path(filePath).read_text()

    def parse_file(self,filePath,root_namespace):
        pass# should be inherited
